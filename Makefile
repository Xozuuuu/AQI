# Makefile cho Hệ thống AQI Monitoring

.PHONY: help install run test clean docker-build docker-run docker-stop deploy

# Mặc định
help:
	@echo "🌍 Hệ thống Giám sát Chất lượng Không khí Thông minh"
	@echo "=================================================="
	@echo ""
	@echo "Các lệnh có sẵn:"
	@echo "  install     - Cài đặt dependencies"
	@echo "  run         - Chạy ứng dụng"
	@echo "  test        - Chạy tests"
	@echo "  clean       - Dọn dẹp files tạm"
	@echo "  docker-build- Build Docker image"
	@echo "  docker-run  - Chạy với Docker"
	@echo "  docker-stop - Dừng Docker containers"
	@echo "  deploy      - Triển khai production"
	@echo ""

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
