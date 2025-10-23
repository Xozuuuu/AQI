# AQI Monitoring System - Professional Makefile

.PHONY: help install install-dev run test test-unit test-integration clean format lint type-check docker-build docker-run docker-stop deploy docs

# Default target
help: ## Show this help message
	@echo "🌍 AQI Monitoring System - Professional Development"
	@echo "=================================================="
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# Installation
install: ## Install production dependencies
	@echo "📦 Installing production dependencies..."
	pip install -r requirements.txt
	@echo "✅ Installation complete!"

install-dev: ## Install development dependencies
	@echo "🛠️  Installing development dependencies..."
	pip install -e ".[dev,docs,monitoring]"
	pre-commit install
	@echo "✅ Development environment ready!"

# Development
run: ## Run the application
	@echo "🚀 Starting AQI Monitoring System..."
	streamlit run app.py --server.port=8501 --server.address=0.0.0.0

run-dev: ## Run in development mode
	@echo "🔧 Starting in development mode..."
	DEBUG=True LOG_LEVEL=DEBUG streamlit run app.py --server.port=8501 --server.address=0.0.0.0

# Testing
test: test-unit test-integration ## Run all tests

test-unit: ## Run unit tests
	@echo "🧪 Running unit tests..."
	pytest tests/unit/ -v --cov=src/aqi_monitoring --cov-report=html --cov-report=term

test-integration: ## Run integration tests
	@echo "🔗 Running integration tests..."
	pytest tests/integration/ -v

test-watch: ## Run tests in watch mode
	@echo "👀 Running tests in watch mode..."
	pytest-watch -- tests/

# Code Quality
format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	black src/ tests/ app.py
	isort src/ tests/ app.py
	@echo "✅ Code formatted!"

lint: ## Lint code with flake8
	@echo "🔍 Linting code..."
	flake8 src/ tests/ app.py
	@echo "✅ Linting complete!"

type-check: ## Type check with mypy
	@echo "🔬 Type checking..."
	mypy src/aqi_monitoring
	@echo "✅ Type checking complete!"

quality: format lint type-check ## Run all quality checks

# Database
db-init: ## Initialize database
	@echo "🗄️  Initializing database..."
	python -c "from src.aqi_monitoring.core.database import AQIDatabase; AQIDatabase()"
	@echo "✅ Database initialized!"

db-migrate: ## Run database migrations
	@echo "🔄 Running database migrations..."
	alembic upgrade head
	@echo "✅ Migrations complete!"

# Documentation
docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	mkdocs build
	@echo "✅ Documentation generated!"

docs-serve: ## Serve documentation locally
	@echo "🌐 Serving documentation..."
	mkdocs serve

# Cleanup
clean: ## Clean temporary files
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	@echo "✅ Cleanup complete!"

# Docker
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t aqi-monitoring:latest .
	@echo "✅ Docker image built!"

docker-run: ## Run with Docker Compose
	@echo "🐳 Starting with Docker Compose..."
	docker-compose up -d
	@echo "✅ Application running at http://localhost:8501"

docker-stop: ## Stop Docker containers
	@echo "🛑 Stopping Docker containers..."
	docker-compose down
	@echo "✅ Containers stopped!"

docker-logs: ## View Docker logs
	@echo "📋 Viewing Docker logs..."
	docker-compose logs -f

# Deployment
deploy: ## Deploy to production
	@echo "🚀 Deploying to production..."
	git pull origin main
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✅ Deployment complete!"

# Data Management
data-fetch: ## Fetch latest AQI data
	@echo "📊 Fetching latest AQI data..."
	python -c "from src.aqi_monitoring.services.data_service import DataService; import asyncio; asyncio.run(DataService().fetch_and_save_aqi_data())"
	@echo "✅ Data fetched!"

data-backup: ## Backup data
	@echo "💾 Backing up data..."
	mkdir -p backups
	tar -czf backups/aqi_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz data/
	@echo "✅ Backup complete!"

# Monitoring
monitor: ## Start monitoring
	@echo "📊 Starting monitoring..."
	python -m aqi_monitoring.monitoring
	@echo "✅ Monitoring started!"

# Security
security-check: ## Run security checks
	@echo "🔒 Running security checks..."
	bandit -r src/
	safety check
	@echo "✅ Security check complete!"

# Performance
profile: ## Profile application performance
	@echo "⚡ Profiling application..."
	python -m cProfile -o profile.stats app.py
	@echo "✅ Profile saved to profile.stats"

# Setup
setup: install-dev db-init ## Complete development setup
	@echo "🎉 Development environment ready!"
	@echo "Run 'make run' to start the application"

# Production setup
setup-prod: install docker-build ## Complete production setup
	@echo "🎉 Production environment ready!"
	@echo "Run 'make docker-run' to start the application"

# Cài đặt dependencies
install:
	@echo "📦 Cài đặt dependencies..."
	pip install -r docs/requirements.txt
	@echo "✅ Hoàn thành!"

# Chạy ứng dụng
run:
	@echo "🚀 Khởi động ứng dụng..."
	python start.py

# Chạy tests
test:
	@echo "🧪 Chạy tests..."
	python test_system.py

# Dọn dẹp
clean:
	@echo "🧹 Dọn dẹp files tạm..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	@echo "✅ Hoàn thành!"

# Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t aqi-monitoring .
	@echo "✅ Build hoàn thành!"

# Chạy với Docker
docker-run:
	@echo "🐳 Chạy với Docker..."
	docker-compose up -d
	@echo "✅ Ứng dụng đang chạy tại http://localhost:8501"

# Dừng Docker containers
docker-stop:
	@echo "🛑 Dừng Docker containers..."
	docker-compose down
	@echo "✅ Đã dừng!"

# Triển khai production
deploy:
	@echo "🚀 Triển khai production..."
	@echo "1. Cập nhật code..."
	git pull origin main
	@echo "2. Build và restart containers..."
	docker-compose down
	docker-compose build --no-cache
	docker-compose up -d
	@echo "3. Kiểm tra status..."
	docker-compose ps
	@echo "✅ Triển khai hoàn thành!"

# Backup dữ liệu
backup:
	@echo "💾 Backup dữ liệu..."
	mkdir -p backups
	tar -czf backups/aqi_backup_$(shell date +%Y%m%d_%H%M%S).tar.gz data/
	@echo "✅ Backup hoàn thành!"

# Restore dữ liệu
restore:
	@echo "📥 Restore dữ liệu..."
	@echo "Vui lòng chỉ định file backup:"
	@echo "make restore-file BACKUP_FILE=backups/aqi_backup_20240115_120000.tar.gz"
	@if [ -z "$(BACKUP_FILE)" ]; then echo "❌ Vui lòng chỉ định BACKUP_FILE"; exit 1; fi
	tar -xzf $(BACKUP_FILE)
	@echo "✅ Restore hoàn thành!"

# Cập nhật dữ liệu
update-data:
	@echo "🔄 Cập nhật dữ liệu..."
	python run.py
	@echo "✅ Cập nhật hoàn thành!"

# Xem logs
logs:
	@echo "📋 Xem logs..."
	docker-compose logs -f aqi-monitoring

# Kiểm tra status
status:
	@echo "📊 Kiểm tra status..."
	docker-compose ps
	@echo ""
	@echo "🌐 Ứng dụng: http://localhost:8501"
	@echo "📊 Health check: http://localhost:8501/_stcore/health"

# Cài đặt development
install-dev:
	@echo "🛠️  Cài đặt development dependencies..."
	pip install -r docs/requirements.txt
	pip install black isort flake8 pytest
	@echo "✅ Hoàn thành!"

# Format code
format:
	@echo "🎨 Format code..."
	black .
	isort .
	@echo "✅ Hoàn thành!"

# Lint code
lint:
	@echo "🔍 Lint code..."
	flake8 .
	@echo "✅ Hoàn thành!"

# Chạy tất cả checks
check: format lint test
	@echo "✅ Tất cả checks hoàn thành!"

# Setup môi trường mới
setup:
	@echo "⚙️  Setup môi trường mới..."
	python -m venv env
	@echo "✅ Tạo virtual environment"
	@echo "📝 Kích hoạt với: source env/bin/activate (Linux/macOS) hoặc env\\Scripts\\activate (Windows)"
	@echo "📦 Cài đặt dependencies: make install"
	@echo "🚀 Chạy ứng dụng: make run"
