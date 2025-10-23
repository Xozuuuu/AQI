# 🚀 Hướng dẫn Sử dụng Nhanh - Hệ thống AQI Monitoring

## ⚡ Khởi động Nhanh (30 giây)

### 1. Chạy ứng dụng
```bash
# Cách 1: Chạy trực tiếp
streamlit run app.py

# Cách 2: Sử dụng script
python start.py

# Cách 3: Demo đầy đủ
python run_demo.py
```

### 2. Truy cập ứng dụng
- **URL**: http://localhost:8501
- **Tự động mở**: Trình duyệt sẽ tự động mở

## 🎯 Sử dụng Cơ bản

### Dashboard (Trang chủ)
1. **Cập nhật dữ liệu**: Click nút "🔄 Cập nhật dữ liệu"
2. **Xem thống kê**: AQI trung bình, cao nhất, thấp nhất
3. **Khám phá bản đồ**: Click vào các điểm để xem chi tiết
4. **Phân tích biểu đồ**: Xem xu hướng và phân bố

### Dự báo
1. Chuyển đến tab "🔮 Dự báo"
2. Chọn số ngày dự báo (1-7 ngày)
3. Đặt ngưỡng cảnh báo AQI
4. Click "🔮 Thực hiện dự báo"
5. Xem kết quả và cảnh báo

### Báo cáo
1. Chuyển đến tab "📈 Báo cáo"
2. Chọn loại báo cáo:
   - **Tổng quan**: Thống kê toàn quốc
   - **Theo tỉnh**: Phân tích chi tiết từng địa phương
   - **So sánh tỉnh**: Đánh giá tương đối
3. Click "📊 Tạo báo cáo"
4. Xuất dữ liệu (Excel/JSON) nếu cần

### Cài đặt
1. Chuyển đến tab "⚙️ Cài đặt"
2. **Quản lý API**: Xem cấu hình API key
3. **Quản lý dữ liệu**: Xóa lịch sử, tạo dữ liệu mẫu
4. **Thông tin hệ thống**: Xem trạng thái và metrics

## 📊 Tính năng Chính

### 🗺️ Bản đồ Tương tác
- **23 tỉnh/thành phố** Việt Nam
- **Màu sắc trực quan** theo mức độ AQI
- **Popup thông tin** chi tiết
- **Tương tác mượt mà** (zoom, pan, click)

### 📈 Biểu đồ Phân tích
- **Biểu đồ cột**: AQI theo tỉnh
- **Biểu đồ tròn**: Phân bố mức độ chất lượng
- **Biểu đồ đường**: Xu hướng theo thời gian
- **Tương tác**: Hover, click, zoom

### 🔮 Dự báo Thông minh
- **Machine Learning**: Polynomial Regression
- **Tích hợp thời tiết**: Điều chỉnh theo yếu tố thời tiết
- **Cảnh báo tự động**: Thông báo khi AQI vượt ngưỡng
- **Dự báo 7 ngày**: Hỗ trợ lập kế hoạch

### 📋 Báo cáo Chi tiết
- **Báo cáo tổng quan**: Thống kê toàn quốc
- **Báo cáo theo tỉnh**: Phân tích chi tiết
- **So sánh tỉnh**: Đánh giá tương đối
- **Xuất dữ liệu**: Excel, JSON

## 🎨 Giao diện

### Màu sắc AQI
| AQI | Mức độ | Màu sắc | Khuyến nghị |
|-----|--------|---------|-------------|
| 0-50 | Tốt | 🟢 Xanh lá | Chất lượng tốt |
| 51-100 | Trung bình | 🟡 Vàng | Nhóm nhạy cảm cẩn thận |
| 101-150 | Không tốt cho nhóm nhạy cảm | 🟠 Cam | Hạn chế hoạt động |
| 151-200 | Không tốt | 🔴 Đỏ | Tránh hoạt động ngoài trời |
| 201-300 | Rất không tốt | 🟣 Tím | Ở trong nhà |
| 300+ | Nguy hiểm | ⚫ Đỏ đậm | Đóng cửa sổ |

### Layout
- **Header**: Tiêu đề và logo
- **Sidebar**: Điều khiển và cài đặt
- **Main area**: Nội dung chính
- **Footer**: Thông tin hệ thống

## 🔧 Cài đặt Nhanh

### Yêu cầu tối thiểu
- Python 3.8+
- 4GB RAM
- 10GB storage

### Cài đặt tự động
```bash
# 1. Clone repository
git clone <repository-url>
cd AQI

# 2. Chạy setup tự động
python setup.py

# 3. Chạy ứng dụng
streamlit run app.py
```

### Cài đặt thủ công
```bash
# 1. Tạo virtual environment
python -m venv env
source env/bin/activate  # Linux/macOS
# hoặc
env\Scripts\activate     # Windows

# 2. Cài đặt dependencies
pip install -r docs/requirements.txt

# 3. Cấu hình
cp env.example .env
# Chỉnh sửa .env với API key thực

# 4. Chạy ứng dụng
streamlit run app.py
```

## 🐳 Docker (Nhanh nhất)

```bash
# 1. Cấu hình
cp env.example .env

# 2. Chạy với Docker
docker-compose up -d

# 3. Truy cập
open http://localhost:8501
```

## 🚨 Xử lý Lỗi Thường gặp

### Lỗi "No module named 'streamlit'"
```bash
pip install streamlit
```

### Lỗi "API key not found"
- Kiểm tra file `.env`
- Đảm bảo `API_KEY` được cấu hình

### Lỗi "Port 8501 already in use"
```bash
# Tìm và kill process
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Lỗi encoding
- Đảm bảo terminal hỗ trợ UTF-8
- Sử dụng PowerShell hoặc Command Prompt mới

## 📱 Mobile & Tablet

### Responsive Design
- **Mobile**: Giao diện tối ưu cho điện thoại
- **Tablet**: Layout phù hợp cho máy tính bảng
- **Desktop**: Trải nghiệm đầy đủ

### Touch Support
- **Swipe**: Vuốt để điều hướng
- **Pinch**: Zoom bản đồ
- **Tap**: Click để xem chi tiết

## 🔄 Cập nhật Dữ liệu

### Tự động
- **Cập nhật mỗi giờ**: Hệ thống tự động lấy dữ liệu mới
- **Thông báo**: Cảnh báo khi AQI vượt ngưỡng

### Thủ công
- **Nút cập nhật**: Click "🔄 Cập nhật dữ liệu"
- **API**: Gọi API trực tiếp
- **File**: Import từ CSV

## 📊 Dữ liệu

### Nguồn
- **API**: World Air Quality Index (waqi.info)
- **23 tỉnh**: Hà Nội, TP.HCM, Đà Nẵng, Cần Thơ, v.v.
- **Cập nhật**: Theo thời gian thực

### Lưu trữ
- **SQLite**: Database phát triển
- **PostgreSQL**: Database production
- **CSV**: Backup dữ liệu
- **GeoJSON**: Dữ liệu địa lý

## 🎯 Tips Sử dụng

### Hiệu quả
1. **Cập nhật thường xuyên**: Để có dữ liệu mới nhất
2. **Sử dụng bộ lọc**: Để tìm kiếm nhanh
3. **Xuất báo cáo**: Để lưu trữ và chia sẻ
4. **Theo dõi cảnh báo**: Để bảo vệ sức khỏe

### Tối ưu
1. **Đóng tab không cần thiết**: Để tiết kiệm RAM
2. **Sử dụng bản đồ**: Để xem tổng quan
3. **Phân tích xu hướng**: Để dự đoán
4. **So sánh tỉnh**: Để đánh giá

## 🆘 Hỗ trợ

### Tài liệu
- **README.md**: Tài liệu chính
- **DEPLOYMENT.md**: Hướng dẫn triển khai
- **SYSTEM_SUMMARY.md**: Tóm tắt hệ thống

### Liên hệ
- **GitHub Issues**: Báo lỗi và đề xuất
- **Email**: support@example.com
- **Discord**: Community server

---

**🎉 Chúc bạn sử dụng hệ thống hiệu quả!**

*Hệ thống AQI Monitoring - Giúp bạn theo dõi chất lượng không khí một cách thông minh*
