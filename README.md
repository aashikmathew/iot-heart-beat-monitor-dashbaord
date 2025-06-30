# IoT Heartbeat Monitor

A FastAPI-based backend service for monitoring IoT device heartbeats and detecting anomalies. This project demonstrates real-world backend development skills including health checks, anomaly detection, metrics collection, and containerization.

## 🚀 Features

- **Real-time Device Monitoring**: Track IoT device status, battery levels, and signal strength
- **Anomaly Detection**: Automatically flag devices as "at-risk" based on timeout and battery thresholds
- **Prometheus Metrics**: Built-in metrics collection for observability
- **Beautiful Dashboard**: Modern HTML dashboard with real-time updates
- **RESTful API**: Complete API for device management and monitoring
- **Docker Support**: Full containerization with docker-compose
- **Optional Grafana Integration**: Advanced visualization and alerting

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   IoT Devices   │───▶│   FastAPI App   │───▶│   PostgreSQL    │
│   (Simulated)   │    │   (Port 8000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Prometheus    │
                       │   (Port 9090)   │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │    Grafana      │
                       │   (Port 3000)   │
                       └─────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Monitoring**: Prometheus, Grafana
- **Containerization**: Docker, Docker Compose
- **Frontend**: HTML, Tailwind CSS, Chart.js
- **Testing**: Python asyncio simulator

## 📦 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd iot-heartbeat-monitor
```

### 2. Start the Services

```bash
# Start all services (FastAPI + PostgreSQL + Prometheus + Grafana)
docker-compose up -d

# Or start just the core services
docker-compose up -d app db
```

### 3. Access the Services

- **Dashboard**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Prometheus Metrics**: http://localhost:8000/metrics
- **Prometheus UI**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

### 4. Test with Simulated Devices

```bash
# Install test dependencies
pip install aiohttp

# Run device simulation
python test_devices.py --duration 10
```

## 📋 API Endpoints

### Device Management

- `POST /heartbeat` - Send device heartbeat
- `GET /devices` - List all devices
- `GET /devices/{device_id}` - Get specific device
- `GET /devices/status/{status}` - Filter devices by status
- `DELETE /devices/{device_id}` - Delete device

### Monitoring

- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /` - HTML dashboard

## 🔧 Configuration

### Environment Variables

```bash
DATABASE_URL=postgresql://iot_user:iot_password@db:5432/iot_heartbeat
```

### Device Status Logic

- **Online**: Device checked in within last 5 minutes
- **At Risk**: Device hasn't checked in within 2 minutes OR battery < 20%
- **Offline**: Device hasn't checked in for more than 5 minutes

## 📊 Monitoring & Metrics

### Prometheus Metrics

- `iot_heartbeat_total` - Total heartbeat requests
- `iot_device_status` - Current device status
- `iot_device_battery_level` - Battery levels
- `iot_device_signal_strength` - Signal strength
- `iot_device_count` - Device count by status

### Grafana Dashboard

The included Grafana dashboard provides:
- Device status overview
- Battery level trends
- Signal strength monitoring
- Heartbeat rate analysis

## 🧪 Testing

### Manual Testing

```bash
# Send a test heartbeat
curl -X POST "http://localhost:8000/heartbeat" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-device-001",
    "name": "Test Sensor",
    "battery_level": 85.5,
    "signal_strength": -45.2,
    "location": "Test Room"
  }'

# Check device status
curl "http://localhost:8000/devices"

# Check health
curl "http://localhost:8000/health"
```

### Automated Testing

```bash
# Run device simulation
python test_devices.py --duration 5 --url http://localhost:8000
```

## 🐳 Docker Commands

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# Clean up volumes
docker-compose down -v
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL container is running: `docker-compose ps`
   - Check logs: `docker-compose logs db`

2. **Port Already in Use**
   - Change ports in `docker-compose.yml`
   - Or stop conflicting services

3. **Prometheus Can't Scrape Metrics**
   - Verify app is running: `curl http://localhost:8000/health`
   - Check Prometheus targets: http://localhost:9090/targets

### Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs app
docker-compose logs db
docker-compose logs prometheus
```

## 📈 Performance

- **FastAPI**: Handles 1000+ requests/second
- **PostgreSQL**: Optimized for IoT time-series data
- **Prometheus**: Efficient metrics storage and querying
- **Auto-scaling**: Ready for horizontal scaling

## 🔐 Security Considerations

- Database credentials in environment variables
- Non-root Docker containers
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy

## 🚀 Production Deployment

### Recommended Setup

1. **Use a reverse proxy** (nginx/traefik)
2. **Enable HTTPS** with Let's Encrypt
3. **Set up monitoring alerts** in Grafana
4. **Use external PostgreSQL** for persistence
5. **Implement rate limiting** for heartbeat endpoints
6. **Add authentication** for API endpoints

### Environment Variables

```bash
# Production settings
DATABASE_URL=postgresql://user:pass@prod-db:5432/iot_heartbeat
LOG_LEVEL=INFO
ENVIRONMENT=production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- SQLAlchemy for robust ORM
- Prometheus for metrics collection
- Grafana for beautiful visualizations
- Docker for containerization

---

**Happy Monitoring! 🚀** 