# ⚙️ Hướng dẫn Cấu hình Hệ thống AQI

## 📋 File `.env` đã được cấu hình

### ✅ Cấu hình hiện tại:
```bash
# API Configuration
API_KEY=081060c06310131e81330c727e76f1998b837d57
PROJECT_ROOT=C:\Do_An_Chuyen_Nganh\AQI

# Database Configuration (Optional - for production)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=aqi_monitoring
DB_USER=aqi_user
DB_PASSWORD=aqi_password

# Application Configuration
DEBUG=False
LOG_LEVEL=INFO
MAX_WORKERS=4

# Security
SECRET_KEY=aqi_monitoring_secret_key_2024_secure

# Monitoring
ENABLE_MONITORING=True
METRICS_PORT=9090
```

## 🔧 Các biến môi trường

### 🔑 **API Configuration**
| Biến | Giá trị | Mô tả |
|------|---------|-------|
| `API_KEY` | `081060c06310131e81330c727e76f1998b837d57` | API key để lấy dữ liệu AQI từ waqi.info |
| `PROJECT_ROOT` | `C:\Do_An_Chuyen_Nganh\AQI` | Đường dẫn gốc của dự án |

### 🗄️ **Database Configuration**
| Biến | Giá trị | Mô tả |
|------|---------|-------|
| `DB_HOST` | `localhost` | Host của database (PostgreSQL) |
| `DB_PORT` | `5432` | Port của database |
| `DB_NAME` | `aqi_monitoring` | Tên database |
| `DB_USER` | `aqi_user` | Username để kết nối database |
| `DB_PASSWORD` | `aqi_password` | Password để kết nối database |

### ⚙️ **Application Configuration**
| Biến | Giá trị | Mô tả |
|------|---------|-------|
| `DEBUG` | `False` | Chế độ debug (True/False) |
| `LOG_LEVEL` | `INFO` | Mức độ log (DEBUG/INFO/WARNING/ERROR) |
| `MAX_WORKERS` | `4` | Số worker tối đa cho xử lý song song |

### 🔒 **Security**
| Biến | Giá trị | Mô tả |
|------|---------|-------|
| `SECRET_KEY` | `aqi_monitoring_secret_key_2024_secure` | Secret key cho bảo mật ứng dụng |

### 📊 **Monitoring**
| Biến | Giá trị | Mô tả |
|------|---------|-------|
| `ENABLE_MONITORING` | `True` | Bật/tắt monitoring |
| `METRICS_PORT` | `9090` | Port cho metrics monitoring |

## 🚀 Cách sử dụng

### 1. **Kiểm tra cấu hình:**
```bash
python -c "from decouple import config; print('API_KEY:', config('API_KEY'))"
```

### 2. **Chạy ứng dụng:**
```bash
streamlit run app.py
```

### 3. **Chạy với Docker:**
```bash
docker-compose up -d
```

## 🔧 Tùy chỉnh cấu hình

### **Thay đổi API Key:**
```bash
# Mở file .env và sửa
API_KEY=your_new_api_key_here
```

### **Thay đổi đường dẫn dự án:**
```bash
# Mở file .env và sửa
PROJECT_ROOT=C:\Your\New\Path\AQI
```

### **Bật chế độ debug:**
```bash
# Mở file .env và sửa
DEBUG=True
LOG_LEVEL=DEBUG
```

## 🛡️ Bảo mật

### ✅ **Đã được bảo vệ:**
- File `.env` đã được thêm vào `.gitignore`
- Không commit thông tin nhạy cảm vào Git
- Secret key đã được tạo an toàn

### 🔒 **Khuyến nghị:**
- **Không chia sẻ** file `.env` với người khác
- **Thay đổi** secret key trong production
- **Sử dụng** biến môi trường hệ thống cho production

## 📊 Kiểm tra cấu hình

### **Test API Key:**
```python
from backend.fetch_aqi import fetch_aqi
df = fetch_aqi()
print(f"Lấy được {len(df)} bản ghi AQI")
```

### **Test Database:**
```python
from backend.database import AQIDatabase
db = AQIDatabase()
print("Database đã sẵn sàng")
```

### **Test toàn bộ hệ thống:**
```bash
python quick_test.py
```

## 🔄 Cập nhật cấu hình

### **Thêm biến mới:**
1. Thêm vào file `.env`
2. Thêm vào file `env.example`
3. Cập nhật code để sử dụng biến mới

### **Ví dụ thêm biến mới:**
```bash
# Trong .env
NEW_FEATURE=True
NEW_API_URL=https://api.example.com

# Trong code
from decouple import config
new_feature = config('NEW_FEATURE', default=False, cast=bool)
new_api_url = config('NEW_API_URL', default='')
```

## 🎯 Cấu hình cho môi trường khác nhau

### **Development:**
```bash
DEBUG=True
LOG_LEVEL=DEBUG
DB_HOST=localhost
```

### **Production:**
```bash
DEBUG=False
LOG_LEVEL=WARNING
DB_HOST=production-db-server
```

### **Testing:**
```bash
DEBUG=True
LOG_LEVEL=DEBUG
DB_NAME=aqi_testing
```

## 📝 Ghi chú

- **File `.env`** chứa cấu hình thực tế
- **File `env.example`** chứa mẫu cấu hình
- **File `.gitignore`** bảo vệ file `.env`
- **Tất cả** biến môi trường đã được cấu hình đúng

---

**🎉 Cấu hình đã hoàn tất! Hệ thống AQI sẵn sàng chạy!**
