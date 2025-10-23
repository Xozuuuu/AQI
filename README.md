# 🌍 Hệ thống Giám sát Chất lượng Không khí Thông minh

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Hệ thống giám sát chất lượng không khí thông minh được xây dựng với Python, Streamlit, Folium và các công nghệ tiên tiến để theo dõi, phân tích và dự báo chất lượng không khí tại Việt Nam.

## ✨ Tính năng chính

### 📊 Dashboard Tương tác
- **Thống kê thời gian thực**: Hiển thị AQI của 23 tỉnh/thành phố
- **Bản đồ tương tác**: Visualize dữ liệu trên bản đồ Việt Nam với Folium
- **Biểu đồ động**: Phân tích xu hướng với Plotly
- **Giao diện responsive**: Tối ưu cho mọi thiết bị

### 🔮 Dự báo Thông minh
- **Machine Learning**: Sử dụng Polynomial Regression để dự báo AQI
- **Tích hợp thời tiết**: Điều chỉnh dự báo dựa trên yếu tố thời tiết
- **Cảnh báo tự động**: Thông báo khi AQI vượt ngưỡng an toàn
- **Dự báo 7 ngày**: Hỗ trợ lập kế hoạch dài hạn

### 📈 Báo cáo và Phân tích
- **Báo cáo tổng quan**: Thống kê toàn quốc
- **Báo cáo theo tỉnh**: Phân tích chi tiết từng địa phương
- **So sánh tỉnh**: Đánh giá tương đối giữa các khu vực
- **Xuất dữ liệu**: Hỗ trợ Excel và JSON

### 🗺️ Bản đồ Địa lý
- **Tọa độ chính xác**: 23 tỉnh/thành phố Việt Nam
- **Màu sắc trực quan**: Phân loại AQI theo tiêu chuẩn quốc tế
- **Popup thông tin**: Chi tiết AQI và thời gian cập nhật
- **Tương tác mượt mà**: Zoom, pan, click để xem chi tiết

## 🚀 Công nghệ sử dụng

### Backend
- **Python 3.11+**: Ngôn ngữ lập trình chính
- **Pandas**: Xử lý và phân tích dữ liệu
- **NumPy**: Tính toán số học và ma trận
- **GeoPandas**: Xử lý dữ liệu địa lý
- **Scikit-learn**: Machine Learning và dự báo

### Frontend
- **Streamlit**: Framework web app tương tác
- **Plotly**: Biểu đồ động và tương tác
- **Folium**: Bản đồ tương tác
- **HTML/CSS**: Giao diện tùy chỉnh

### Data & Storage
- **SQLite**: Database phát triển
- **PostgreSQL**: Database production
- **CSV**: Lưu trữ dữ liệu thô
- **GeoJSON**: Dữ liệu địa lý

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Orchestration
- **Nginx**: Reverse proxy
- **SSL/TLS**: Bảo mật

## 📦 Cài đặt

### Yêu cầu hệ thống
- Python 3.11+
- 4GB RAM (khuyến nghị 8GB+)
- 10GB storage (khuyến nghị 50GB+)

### Cài đặt nhanh

```bash
# 1. Clone repository
git clone https://github.com/your-username/aqi-monitoring.git
cd aqi-monitoring

# 2. Tạo virtual environment
python -m venv env
source env/bin/activate  # Linux/macOS
# hoặc
env\Scripts\activate     # Windows

# 3. Cài đặt dependencies
pip install -r docs/requirements.txt

# 4. Cấu hình API key
cp env.example .env
# Chỉnh sửa .env với API key thực

# 5. Chạy ứng dụng
streamlit run app.py
```

Truy cập: http://localhost:8501

### Cài đặt với Docker

```bash
# 1. Clone và cấu hình
git clone https://github.com/your-username/aqi-monitoring.git
cd aqi-monitoring
cp env.example .env

# 2. Chạy với Docker Compose
docker-compose up -d

# 3. Truy cập ứng dụng
open http://localhost:8501
```

## 🎯 Sử dụng

### Dashboard Chính
1. **Cập nhật dữ liệu**: Click "🔄 Cập nhật dữ liệu" để lấy dữ liệu mới nhất
2. **Xem thống kê**: Theo dõi AQI trung bình, cao nhất, thấp nhất
3. **Khám phá bản đồ**: Click vào các điểm để xem chi tiết
4. **Phân tích biểu đồ**: Xem xu hướng và phân bố AQI

### Dự báo
1. Chuyển đến tab "🔮 Dự báo"
2. Chọn số ngày dự báo (1-7 ngày)
3. Đặt ngưỡng cảnh báo AQI
4. Click "🔮 Thực hiện dự báo"
5. Xem kết quả và cảnh báo

### Báo cáo
1. Chuyển đến tab "📈 Báo cáo"
2. Chọn loại báo cáo (Tổng quan/Theo tỉnh/So sánh)
3. Click "📊 Tạo báo cáo"
4. Xuất dữ liệu (Excel/JSON)

## 📊 Dữ liệu

### Nguồn dữ liệu
- **API AQI**: World Air Quality Index (waqi.info)
- **23 tỉnh/thành**: Hà Nội, TP.HCM, Đà Nẵng, Cần Thơ, v.v.
- **Cập nhật**: Theo thời gian thực từ API

### Cấu trúc dữ liệu
```json
{
  "Province": "Ha Noi",
  "AQI": 85,
  "Date": "2024-01-15T10:30:00",
  "Category": "Trung bình"
}
```

### Phân loại AQI
| AQI | Mức độ | Màu sắc | Khuyến nghị |
|-----|--------|---------|-------------|
| 0-50 | Tốt | Xanh lá | Chất lượng không khí tốt |
| 51-100 | Trung bình | Vàng | Nhóm nhạy cảm nên cẩn thận |
| 101-150 | Không tốt cho nhóm nhạy cảm | Cam | Nhóm nhạy cảm nên hạn chế hoạt động |
| 151-200 | Không tốt | Đỏ | Mọi người nên hạn chế hoạt động ngoài trời |
| 201-300 | Rất không tốt | Tím | Tránh hoạt động ngoài trời |
| 300+ | Nguy hiểm | Đỏ đậm | Ở trong nhà, đóng cửa sổ |

## 🔧 Cấu hình

### Environment Variables
```bash
# API Configuration
API_KEY=your_aqi_api_key_here
PROJECT_ROOT=/app

# Database (Optional)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aqi_monitoring
DB_USER=aqi_user
DB_PASSWORD=aqi_password

# Application
DEBUG=False
LOG_LEVEL=INFO
```

### Cấu hình Streamlit
```toml
# .streamlit/config.toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

## 🚀 Triển khai Production

Xem [DEPLOYMENT.md](DEPLOYMENT.md) để biết hướng dẫn chi tiết về triển khai production.

### Tóm tắt nhanh
```bash
# 1. Chuẩn bị server
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Deploy application
git clone <repository-url>
cd aqi-monitoring
cp env.example .env
# Chỉnh sửa .env
docker-compose up -d

# 3. Cấu hình Nginx (optional)
sudo apt install nginx -y
# Cấu hình reverse proxy
```

## 📈 Performance

### Benchmarks
- **Thời gian tải**: < 2 giây
- **Memory usage**: ~200MB
- **API response**: < 1 giây
- **Concurrent users**: 100+

### Optimization
- Caching dữ liệu
- Lazy loading
- Database indexing
- CDN cho static files

## 🤝 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng:

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

### Development Setup
```bash
# Cài đặt development dependencies
pip install -r docs/requirements-dev.txt

# Chạy tests
pytest tests/

# Code formatting
black .
isort .

# Linting
flake8 .
```

## 📝 License

Dự án này được phân phối dưới MIT License. Xem [LICENSE](LICENSE) để biết thêm thông tin.

## 🙏 Acknowledgments

- [World Air Quality Index](https://waqi.info/) - Nguồn dữ liệu AQI
- [Streamlit](https://streamlit.io/) - Framework web app
- [Folium](https://python-visualization.github.io/folium/) - Bản đồ tương tác
- [Plotly](https://plotly.com/) - Biểu đồ tương tác
- [GeoPandas](https://geopandas.org/) - Xử lý dữ liệu địa lý

## 📞 Support

- **Documentation**: [Wiki](https://github.com/your-username/aqi-monitoring/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-username/aqi-monitoring/issues)
- **Email**: support@example.com
- **Discord**: [Community Server](https://discord.gg/your-server)

## 🔮 Roadmap

### Version 2.0
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] Historical data analysis
- [ ] Multi-language support
- [ ] Advanced ML models

### Version 2.1
- [ ] Weather integration
- [ ] Traffic data correlation
- [ ] Health recommendations
- [ ] Social sharing
- [ ] API endpoints

---

**Được phát triển với ❤️ bởi team AQI Monitoring**

*Giúp chúng ta xây dựng một tương lai với không khí sạch hơn!*
