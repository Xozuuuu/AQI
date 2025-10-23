# Hướng dẫn Triển khai Hệ thống Giám sát Chất lượng Không khí

## Tổng quan

Hệ thống Giám sát Chất lượng Không khí Thông minh được xây dựng với các công nghệ:
- **Frontend**: Streamlit
- **Backend**: Python, Pandas, NumPy
- **Bản đồ**: Folium, GeoPandas
- **Machine Learning**: Scikit-learn
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Deployment**: Docker, Docker Compose

## Yêu cầu Hệ thống

### Tối thiểu
- CPU: 2 cores
- RAM: 4GB
- Storage: 10GB
- OS: Linux/Windows/macOS

### Khuyến nghị
- CPU: 4+ cores
- RAM: 8GB+
- Storage: 50GB+
- OS: Ubuntu 20.04+ / CentOS 8+

## Cài đặt Local Development

### 1. Clone Repository
```bash
git clone <repository-url>
cd AQI
```

### 2. Tạo Virtual Environment
```bash
# Windows
python -m venv env
env\Scripts\activate

# Linux/macOS
python3 -m venv env
source env/bin/activate
```

### 3. Cài đặt Dependencies
```bash
pip install -r docs/requirements.txt
```

### 4. Cấu hình Environment
```bash
# Copy file cấu hình mẫu
cp env.example .env

# Chỉnh sửa file .env với API key thực
# API_KEY=your_actual_api_key_here
```

### 5. Chạy Ứng dụng
```bash
streamlit run app.py
```

Truy cập: http://localhost:8501

## Triển khai với Docker

### 1. Build Docker Image
```bash
docker build -t aqi-monitoring .
```

### 2. Chạy Container
```bash
docker run -d \
  --name aqi-monitoring \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -e API_KEY=your_api_key \
  aqi-monitoring
```

### 3. Sử dụng Docker Compose
```bash
# Tạo file .env
cp env.example .env
# Chỉnh sửa .env với thông tin thực

# Chạy tất cả services
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng services
docker-compose down
```

## Triển khai Production

### 1. Chuẩn bị Server

#### Ubuntu 20.04+
```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Cài đặt Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Cài đặt Nginx (optional)
sudo apt install nginx -y
```

### 2. Cấu hình SSL (Optional)
```bash
# Sử dụng Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y

# Tạo certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Thêm dòng: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 3. Deploy Application
```bash
# Clone repository
git clone <repository-url>
cd AQI

# Cấu hình environment
cp env.example .env
nano .env  # Chỉnh sửa với thông tin production

# Chạy application
docker-compose -f docker-compose.yml up -d

# Kiểm tra status
docker-compose ps
docker-compose logs -f aqi-monitoring
```

### 4. Cấu hình Nginx (Production)
```bash
# Tạo file cấu hình Nginx
sudo nano /etc/nginx/sites-available/aqi-monitoring

# Nội dung:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/aqi-monitoring /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Monitoring và Maintenance

### 1. Health Checks
```bash
# Kiểm tra container status
docker ps

# Kiểm tra logs
docker-compose logs -f aqi-monitoring

# Kiểm tra health endpoint
curl http://localhost:8501/_stcore/health
```

### 2. Backup Data
```bash
# Backup database
docker exec aqi-monitoring_postgres_1 pg_dump -U aqi_user aqi_monitoring > backup.sql

# Backup data directory
tar -czf data_backup_$(date +%Y%m%d).tar.gz data/
```

### 3. Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild và restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 4. Monitoring với Prometheus (Optional)
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'aqi-monitoring'
    static_configs:
      - targets: ['localhost:8501']
```

## Troubleshooting

### Lỗi thường gặp

#### 1. Container không start
```bash
# Kiểm tra logs
docker-compose logs aqi-monitoring

# Kiểm tra port conflict
netstat -tulpn | grep 8501
```

#### 2. Lỗi API Key
```bash
# Kiểm tra environment variables
docker exec aqi-monitoring env | grep API_KEY

# Cập nhật API key
docker-compose down
# Chỉnh sửa .env
docker-compose up -d
```

#### 3. Lỗi database connection
```bash
# Kiểm tra PostgreSQL
docker-compose logs postgres

# Reset database
docker-compose down -v
docker-compose up -d
```

#### 4. Lỗi memory
```bash
# Kiểm tra memory usage
docker stats

# Tăng memory limit trong docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
```

### Performance Tuning

#### 1. Streamlit Configuration
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

#### 2. Database Optimization
```sql
-- Tạo indexes cho performance
CREATE INDEX idx_daily_aqi_date ON daily_aqi(Date);
CREATE INDEX idx_daily_aqi_province ON daily_aqi(Province);
CREATE INDEX idx_daily_aqi_aqi ON daily_aqi(AQI);
```

## Security Best Practices

### 1. Environment Variables
- Không commit file .env
- Sử dụng secrets management
- Rotate API keys định kỳ

### 2. Network Security
- Sử dụng HTTPS
- Cấu hình firewall
- Giới hạn access IP

### 3. Container Security
- Sử dụng non-root user
- Scan vulnerabilities
- Update base images

## Scaling

### Horizontal Scaling
```yaml
# docker-compose.yml
services:
  aqi-monitoring:
    deploy:
      replicas: 3
    # ... other config
```

### Load Balancing
```nginx
upstream streamlit {
    server aqi-monitoring-1:8501;
    server aqi-monitoring-2:8501;
    server aqi-monitoring-3:8501;
}
```

## Support

- **Documentation**: [Link to docs]
- **Issues**: [GitHub Issues]
- **Email**: support@example.com

## License

MIT License - Xem file LICENSE để biết thêm chi tiết.
