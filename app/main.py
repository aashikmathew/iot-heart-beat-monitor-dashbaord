from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func, text
import time
from datetime import datetime, timedelta

from .database import get_db, engine, wait_for_db, Base
from .models import Device, Base
from .schemas import HeartbeatRequest, DeviceResponse, DeviceListResponse, HealthResponse
from .metrics import heartbeat_counter, heartbeat_latency, update_device_metrics, get_metrics

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="IoT Heartbeat Monitor",
    description="A FastAPI-based backend service for monitoring IoT device heartbeats and detecting anomalies",
    version="1.0.0"
)

# Templates for HTML dashboard
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    """Wait for database to be ready on startup"""
    print("🚀 Starting IoT Heartbeat Monitor...")
    print("⏳ Waiting for database connection...")
    
    if wait_for_db():
        print("✅ Database connection established")
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified")
    else:
        print("❌ Failed to connect to database - continuing anyway")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Main dashboard showing device status"""
    # Update metrics
    update_device_metrics(db)
    
    # Get all devices with updated status
    devices = db.query(Device).all()
    for device in devices:
        device.update_status()
    
    # Count devices by status
    status_counts = {'online': 0, 'offline': 0, 'at-risk': 0}
    for device in devices:
        status_counts[device.status] += 1
    
    # Get recent activity (devices that checked in within last hour)
    recent_activity = db.query(Device).filter(
        Device.last_seen >= datetime.utcnow() - timedelta(hours=1)
    ).count()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "devices": devices,
            "status_counts": status_counts,
            "total_devices": len(devices),
            "recent_activity": recent_activity
        }
    )

@app.post("/heartbeat", response_model=DeviceResponse)
async def receive_heartbeat(
    heartbeat: HeartbeatRequest,
    db: Session = Depends(get_db)
):
    """Receive heartbeat from IoT device"""
    start_time = time.time()
    
    try:
        # Check if device exists
        device = db.query(Device).filter(Device.device_id == heartbeat.device_id).first()
        
        if device:
            # Update existing device
            device.last_seen = datetime.utcnow()
            if heartbeat.name:
                device.name = heartbeat.name
            if heartbeat.battery_level is not None:
                device.battery_level = heartbeat.battery_level
            if heartbeat.signal_strength is not None:
                device.signal_strength = heartbeat.signal_strength
            if heartbeat.location:
                device.location = heartbeat.location
        else:
            # Create new device
            device = Device(
                device_id=heartbeat.device_id,
                name=heartbeat.name,
                battery_level=heartbeat.battery_level,
                signal_strength=heartbeat.signal_strength,
                location=heartbeat.location,
                last_seen=datetime.utcnow()
            )
            db.add(device)
        
        # Update device status
        device.update_status()
        db.commit()
        db.refresh(device)
        
        # Update metrics
        heartbeat_counter.labels(
            device_id=device.device_id,
            status=device.status
        ).inc()
        
        heartbeat_latency.labels(device_id=device.device_id).observe(
            time.time() - start_time
        )
        
        return device
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing heartbeat: {str(e)}")

@app.get("/devices", response_model=DeviceListResponse)
async def list_devices(db: Session = Depends(get_db)):
    """List all devices with their current status"""
    # Update metrics
    update_device_metrics(db)
    
    devices = db.query(Device).all()
    
    # Update status for all devices
    for device in devices:
        device.update_status()
    
    # Count devices by status
    status_counts = {'online': 0, 'offline': 0, 'at-risk': 0}
    for device in devices:
        status_counts[device.status] += 1
    
    return DeviceListResponse(
        devices=devices,
        total_count=len(devices),
        online_count=status_counts['online'],
        offline_count=status_counts['offline'],
        at_risk_count=status_counts['at-risk']
    )

@app.get("/devices/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: str, db: Session = Depends(get_db)):
    """Get specific device details"""
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device.update_status()
    return device

@app.get("/devices/status/{status}")
async def get_devices_by_status(status: str, db: Session = Depends(get_db)):
    """Get devices filtered by status"""
    if status not in ['online', 'offline', 'at-risk']:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    devices = db.query(Device).all()
    filtered_devices = []
    
    for device in devices:
        device.update_status()
        if device.status == status:
            filtered_devices.append(device)
    
    return {"devices": filtered_devices, "count": len(filtered_devices)}

@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection using proper SQLAlchemy syntax
        db.execute(text("SELECT 1"))
        database_connected = True
        total_devices = db.query(func.count(Device.id)).scalar()
    except Exception as e:
        database_connected = False
        total_devices = 0
    
    return HealthResponse(
        status="healthy" if database_connected else "unhealthy",
        timestamp=datetime.utcnow(),
        database_connected=database_connected,
        total_devices=total_devices
    )

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return get_metrics()

@app.delete("/devices/{device_id}")
async def delete_device(device_id: str, db: Session = Depends(get_db)):
    """Delete a device"""
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 