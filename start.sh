#!/bin/bash

# IoT Heartbeat Monitor Startup Script

set -e

echo "🚀 Starting IoT Heartbeat Monitor..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it and try again."
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping services..."
    docker-compose down
    echo "✅ Services stopped."
}

# Set trap to cleanup on script exit
trap cleanup EXIT

# Build and start services
echo "📦 Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ FastAPI service is running"
else
    echo "❌ FastAPI service is not responding"
    exit 1
fi

echo ""
echo "🎉 IoT Heartbeat Monitor is ready!"
echo ""
echo "📊 Access Points:"
echo "   Dashboard:     http://localhost:8000"
echo "   API Docs:      http://localhost:8000/docs"
echo "   Health Check:  http://localhost:8000/health"
echo "   Prometheus:    http://localhost:9090"
echo "   Grafana:       http://localhost:3000 (admin/admin)"
echo ""
echo "🧪 To test with simulated devices:"
echo "   pip install aiohttp"
echo "   python test_devices.py --duration 10"
echo ""
echo "🛑 Press Ctrl+C to stop all services"

# Keep the script running
wait 