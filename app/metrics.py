from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
from sqlalchemy.orm import Session
from .models import Device
from datetime import datetime, timedelta

# Metrics definitions
heartbeat_counter = Counter(
    'iot_heartbeat_total',
    'Total number of heartbeat requests received',
    ['device_id', 'status']
)

device_status_gauge = Gauge(
    'iot_device_status',
    'Current status of IoT devices',
    ['device_id', 'status']
)

battery_level_gauge = Gauge(
    'iot_device_battery_level',
    'Battery level of IoT devices',
    ['device_id']
)

signal_strength_gauge = Gauge(
    'iot_device_signal_strength',
    'Signal strength of IoT devices',
    ['device_id']
)

device_count_gauge = Gauge(
    'iot_device_count',
    'Total number of devices by status',
    ['status']
)

heartbeat_latency = Histogram(
    'iot_heartbeat_latency_seconds',
    'Time taken to process heartbeat requests',
    ['device_id']
)

def update_device_metrics(db: Session):
    """Update Prometheus metrics based on current device states"""
    devices = db.query(Device).all()
    
    # Reset all gauges
    device_status_gauge.clear()
    battery_level_gauge.clear()
    signal_strength_gauge.clear()
    device_count_gauge.clear()
    
    status_counts = {'online': 0, 'offline': 0, 'at-risk': 0}
    
    for device in devices:
        # Update device status
        device.update_status()
        
        # Set status gauge
        device_status_gauge.labels(device_id=device.device_id, status=device.status).set(1)
        
        # Set battery level gauge
        if device.battery_level is not None:
            battery_level_gauge.labels(device_id=device.device_id).set(device.battery_level)
        
        # Set signal strength gauge
        if device.signal_strength is not None:
            signal_strength_gauge.labels(device_id=device.device_id).set(device.signal_strength)
        
        # Count devices by status
        status_counts[device.status] += 1
    
    # Set count gauges
    for status, count in status_counts.items():
        device_count_gauge.labels(status=status).set(count)

def get_metrics():
    """Return Prometheus metrics"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    ) 