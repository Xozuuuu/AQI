# backend/hourly_forecast.py
from datetime import datetime, timedelta
import numpy as np

def get_hourly_forecast(province_name: str):
    """
    Trả về dự báo AQI 6 điểm trong ngày hôm nay (cách 4 tiếng)
    Sau này có thể lấy từ WAQI hourly forecast (có thật!)
    """
    np.random.seed(hash(province_name) % 2**32)
    
    today = datetime.now().date()
    hours = [0, 4, 8, 12, 16, 20]  # 00:00, 04:00, 08:00, 12:00, 16:00, 20:00
    labels = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"]
    display_labels = ["Bây giờ", "4:00 AM", "8:00 AM", "12:00 PM", "4:00 PM", "8:00 PM"]
    
    # Tạo đường cong tự nhiên (giống thực tế: sáng cao, trưa giảm, tối tăng lại)
    base_pattern = [100, 85, 120, 90, 75, 95]
    noise = np.random.randint(-25, 25, size=6)
    aqi_values = np.clip(base_pattern + noise + np.random.randint(-15, 15), 10, 300)
    
    data = []
    for i, h in enumerate(hours):
        time_obj = datetime.combine(today, datetime.min.time()) + timedelta(hours=h)
        aqi = int(aqi_values[i])
        status = get_status(aqi)
        color = get_color(aqi)
        
        data.append({
            "time": time_obj,
            "hour_label": labels[i],
            "display_label": display_labels[i],
            "aqi": aqi,
            "status": status,
            "color": color,
            "icon": get_icon_name(status)
        })
    
    return data

def get_status(aqi):
    if aqi <= 50: return "Tốt"
    elif aqi <= 100: return "Trung bình"
    elif aqi <= 150: return "Kém"
    elif aqi <= 200: return "Xấu"
    elif aqi <= 300: return "Rất xấu"
    else: return "Nguy hại"

def get_color(aqi):
    if aqi <= 50: return "#00e400"
    elif aqi <= 100: return "#cccc16"
    elif aqi <= 150: return "#ff7e00"
    elif aqi <= 200: return "#ff0000"
    elif aqi <= 300: return "#99004c"
    else: return "#4d0000"

def get_icon_name(status):
    return {
        "Tốt": "smile",
        "Trung bình": "neutral",
        "Kém": "frown",
        "Xấu": "sad",
        "Rất xấu": "angry",
        "Nguy hại": "danger"
    }.get(status, "neutral")