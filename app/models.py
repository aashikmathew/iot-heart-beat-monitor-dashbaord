from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime, timedelta

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    status = Column(String, default="offline")  # online, offline, at-risk
    last_seen = Column(DateTime, default=func.now())
    battery_level = Column(Float, nullable=True)  # 0.0 to 100.0
    signal_strength = Column(Float, nullable=True)  # dBm values
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def is_online(self, timeout_minutes=5):
        """Check if device is online based on last seen timestamp"""
        if not self.last_seen:
            return False
        return datetime.utcnow() - self.last_seen < timedelta(minutes=timeout_minutes)
    
    def is_at_risk(self, timeout_minutes=2, battery_threshold=20.0):
        """Check if device is at risk based on timeout and battery level"""
        if not self.last_seen:
            return True
        
        # Check if device hasn't been seen recently
        time_since_last_seen = datetime.utcnow() - self.last_seen
        if time_since_last_seen > timedelta(minutes=timeout_minutes):
            return True
        
        # Check if battery is low
        if self.battery_level is not None and self.battery_level < battery_threshold:
            return True
            
        return False
    
    def update_status(self):
        """Update device status based on current conditions"""
        if self.is_online():
            if self.is_at_risk():
                self.status = "at-risk"
            else:
                self.status = "online"
        else:
            self.status = "offline" 