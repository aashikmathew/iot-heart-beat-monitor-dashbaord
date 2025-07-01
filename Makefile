.PHONY: help build up down logs clean test simulate

# Default target
help:
	@echo "IoT Heartbeat Monitor - Available Commands:"
	@echo ""
	@echo "  build     - Build Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  logs      - View service logs"
	@echo "  clean     - Remove containers and volumes"
	@echo "  test      - Run device simulation"
	@echo "  simulate  - Run device simulation (alias for test)"
	@echo "  health    - Check service health"
	@echo "  install   - Install Python dependencies"
	@echo ""

# Build Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Clean up everything
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Run device simulation
test:
	@echo "🧪 Running device simulation..."
	@echo "Make sure the services are running first: make up"
	@echo ""
	python test_devices.py --duration 5

# Alias for test
simulate: test

# Check service health
health:
	@echo "🔍 Checking service health..."
	@curl -f http://localhost:8000/health || echo "❌ Service not responding"
	@echo "📊 Dashboard: http://localhost:8000"
	@echo "📚 API Docs:  http://localhost:8000/docs"

# Install Python dependencies
install:
	pip install -r requirements.txt
	pip install aiohttp

# Quick start (build + up + health check)
start: build up
	@echo "⏳ Waiting for services to start..."
	@sleep 10
	@make health

# Development mode (with volume mounting for live reload)
dev:
	docker-compose -f docker-compose.yml up --build

# Production mode (without development volumes)
prod:
	docker-compose -f docker-compose.yml up -d --build

# Show running containers
ps:
	docker-compose ps

# Restart services
restart: down up

# Update and restart
update: down build up 