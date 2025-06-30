from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class HeartbeatRequest(BaseModel):
    device_id: str = Field(..., description="Unique device identifier")
    name: Optional[str] = Field(None, description="Human-readable device name")
    battery_level: Optional[float] = Field(None, ge=0.0, le=100.0, description="Battery level percentage")
    signal_strength: Optional[float] = Field(None, description="Signal strength in dBm")
    location: Optional[str] = Field(None, description="Device location")

class DeviceResponse(BaseModel):
    id: int
    device_id: str
    name: Optional[str]
    status: str
    last_seen: datetime
    battery_level: Optional[float]
    signal_strength: Optional[float]
    location: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DeviceListResponse(BaseModel):
    devices: List[DeviceResponse]
    total_count: int
    online_count: int
    offline_count: int
    at_risk_count: int

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database_connected: bool
    total_devices: int 