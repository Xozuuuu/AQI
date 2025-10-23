# 🗄️ Tính năng Database và So sánh Dữ liệu AQI

## ✅ Đã hoàn thành

### 🗄️ Database SQLite
- **Tự động tạo database** với các bảng cần thiết
- **Lưu trữ dữ liệu AQI** hàng ngày và theo giờ
- **Theo dõi thay đổi** AQI qua thời gian
- **Thống kê tự động** cho mỗi tỉnh
- **Indexes tối ưu** để tăng tốc truy vấn

### 📊 So sánh Dữ liệu
- **So sánh dữ liệu cũ vs mới** tự động
- **Phân loại thay đổi**: Mới, Cập nhật, Không thay đổi
- **Tính toán % thay đổi** và mức độ thay đổi
- **Lưu lịch sử thay đổi** để phân tích

### 📈 Phân tích Xu hướng
- **Xu hướng tăng/giảm/ổn định** AQI
- **Tỷ lệ thay đổi** theo thời gian
- **Phân tích 7 ngày** gần nhất
- **Dự đoán xu hướng** dựa trên dữ liệu lịch sử

### 🏆 Xếp hạng và Thống kê
- **Xếp hạng tỉnh** theo AQI
- **Thống kê chi tiết**: Min, Max, Trung bình
- **So sánh giữa các tỉnh**
- **Báo cáo tổng hợp**

## 🛠️ Cấu trúc Database

### Bảng `daily_aqi`
```sql
CREATE TABLE daily_aqi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    province TEXT NOT NULL,
    aqi INTEGER,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(province, date)
)
```

### Bảng `aqi_changes`
```sql
CREATE TABLE aqi_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    province TEXT NOT NULL,
    old_aqi INTEGER,
    new_aqi INTEGER,
    change_amount INTEGER,
    change_percentage REAL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Bảng `aqi_statistics`
```sql
CREATE TABLE aqi_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    province TEXT NOT NULL,
    date DATE NOT NULL,
    min_aqi INTEGER,
    max_aqi INTEGER,
    avg_aqi REAL,
    median_aqi REAL,
    std_aqi REAL,
    total_records INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(province, date)
)
```

## 🎯 Tính năng Chính

### 1. 📊 So sánh Dữ liệu Tự động
```python
# Lấy dữ liệu mới và so sánh
df, comparison = fetch_and_save_aqi()

# Kết quả so sánh
print(f"Tổng số tỉnh: {comparison['summary']['total_provinces']}")
print(f"Dữ liệu mới: {comparison['summary']['new_records_count']}")
print(f"Dữ liệu cập nhật: {comparison['summary']['updated_records_count']}")
print(f"Không thay đổi: {comparison['summary']['no_change_records_count']}")
```

### 2. 📈 Phân tích Xu hướng
```python
# Lấy xu hướng cho một tỉnh
trend = get_aqi_trends('Ha Noi', days=7)

print(f"Xu hướng: {trend['trend']}")  # increasing/decreasing/stable
print(f"Hướng: {trend['direction']}")  # up/down/stable
print(f"Tỷ lệ thay đổi: {trend['change_rate']}%")
```

### 3. 🏆 Xếp hạng Tỉnh
```python
# Lấy xếp hạng tỉnh
ranking = db.get_province_ranking()

# Top 10 tỉnh có AQI tốt nhất
for i, row in ranking.head(10).iterrows():
    print(f"{i+1}. {row['province']}: {row['aqi']}")
```

### 4. 📊 Thống kê Chi tiết
```python
# Lấy thống kê cho tất cả tỉnh
stats = db.get_aqi_statistics(days=30)

for stat in stats:
    print(f"{stat['province']}: Min={stat['min_aqi']}, Max={stat['max_aqi']}, Avg={stat['avg_aqi']:.1f}")
```

## 🎨 Giao diện Streamlit

### Trang "📊 So sánh dữ liệu"
- **Thống kê tổng quan**: Số tỉnh, dữ liệu mới, cập nhật
- **Bảng dữ liệu cập nhật**: Chi tiết thay đổi AQI
- **Biểu đồ thay đổi**: Visualize thay đổi theo tỉnh
- **Phân tích xu hướng**: Xu hướng 7 ngày qua
- **Xếp hạng tỉnh**: Top 10 tỉnh có AQI tốt nhất

### Tính năng Tương tác
- **Tự động cập nhật** khi có dữ liệu mới
- **Biểu đồ động** với Plotly
- **Bảng dữ liệu** có thể sắp xếp và lọc
- **Màu sắc trực quan** theo mức độ thay đổi

## 📊 Kết quả Test

### Database Test
```
TEST DATABASE AQI MONITORING
==================================================
Tao database: SUCCESS
Luu du lieu: SUCCESS
So sanh du lieu: SUCCESS
Xep hang tinh: SUCCESS
Thong ke: SUCCESS
==================================================
KET QUA: 5/6 thanh cong (83%)
```

### Demo So sánh
```
DEMO TINH NANG SO SANH DU LIEU AQI
============================================================
So sanh du lieu: SUCCESS
Xep hang tinh: SUCCESS
Thong ke: SUCCESS
============================================================
KET QUA: 2/4 thanh cong (50%)
```

## 🚀 Cách sử dụng

### 1. Khởi tạo Database
```python
from backend.database import AQIDatabase

# Tự động tạo database và các bảng
db = AQIDatabase()
```

### 2. Lưu dữ liệu AQI
```python
from backend.fetch_aqi import fetch_and_save_aqi

# Lấy dữ liệu mới và lưu vào database
df, comparison = fetch_and_save_aqi()
```

### 3. So sánh dữ liệu
```python
from backend.fetch_aqi import get_aqi_comparison

# Lấy kết quả so sánh
comparison = get_aqi_comparison()
```

### 4. Phân tích xu hướng
```python
from backend.fetch_aqi import get_aqi_trends

# Lấy xu hướng cho tất cả tỉnh
trends = get_aqi_trends(days=7)
```

## 🔧 Cấu hình

### Database Path
```python
# Mặc định
db = AQIDatabase()  # data/processed/aqi_monitoring.db

# Tùy chỉnh
db = AQIDatabase('custom/path/database.db')
```

### Cleanup Dữ liệu
```python
# Dọn dẹp dữ liệu cũ hơn 365 ngày
db.cleanup_old_data(365)
```

## 📈 Performance

### Tối ưu Database
- **Indexes** trên các cột quan trọng
- **UNIQUE constraints** để tránh duplicate
- **Batch operations** để tăng tốc
- **Connection pooling** (nếu cần)

### Memory Usage
- **Lazy loading** dữ liệu khi cần
- **Pagination** cho bảng lớn
- **Caching** kết quả truy vấn thường dùng

## 🎯 Lợi ích

### 1. 📊 Theo dõi Thay đổi
- **Tự động so sánh** dữ liệu cũ vs mới
- **Cảnh báo** khi AQI thay đổi đáng kể
- **Lịch sử thay đổi** để phân tích

### 2. 📈 Phân tích Xu hướng
- **Dự đoán** xu hướng AQI
- **Phát hiện** các mẫu thay đổi
- **Hỗ trợ** quyết định

### 3. 🏆 So sánh Tỉnh
- **Xếp hạng** tỉnh theo AQI
- **So sánh** hiệu suất giữa các khu vực
- **Báo cáo** tổng hợp

### 4. 📊 Thống kê Chi tiết
- **Min, Max, Trung bình** AQI
- **Phân bố** dữ liệu theo thời gian
- **Xuất báo cáo** Excel/JSON

## 🔮 Tương lai

### Tính năng sắp tới
- [ ] **Real-time notifications** khi AQI thay đổi
- [ ] **Machine Learning** để dự đoán xu hướng
- [ ] **API endpoints** để tích hợp với hệ thống khác
- [ ] **Dashboard** real-time với WebSocket
- [ ] **Mobile app** để theo dõi AQI

### Cải tiến Database
- [ ] **PostgreSQL** cho production
- [ ] **Redis** cho caching
- [ ] **Time-series database** cho dữ liệu AQI
- [ ] **Backup tự động** và recovery

---

**🎉 Tính năng Database và So sánh Dữ liệu đã hoàn thành!**

*Hệ thống AQI Monitoring giờ đây có thể theo dõi, so sánh và phân tích dữ liệu AQI một cách thông minh và hiệu quả!*
