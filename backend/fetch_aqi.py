import requests
import pandas as pd
from datetime import datetime
import sys
import os
from decouple import config  # ✅ Dùng để đọc .env

# ✅ Lấy đường dẫn gốc dự án từ .env
project_root = config('PROJECT_ROOT')
sys.path.append(os.path.normpath(project_root))  # Đảm bảo path không lỗi dù có dấu cách

import config  # Import cấu hình sau khi thêm project_root vào path
from backend.database import AQIDatabase


def fetch_aqi():
    aqi_data = []
    for province in config.PROVINCES_LIST:
        url = f'https://api.waqi.info/feed/{province}/?token={config.API_KEY}'
        response = requests.get(url).json()
        print("Response for", province, ":", response)  # Debug

        if response.get('status') == 'ok' and isinstance(response.get('data'), dict):
            aqi = response['data'].get('aqi')
            if aqi in ('-', None, ''):
                aqi = None
                print(f"Cảnh báo: AQI thiếu cho {province}.")
        else:
            aqi = None

        aqi_data.append({
            'Province': config.PROVINCE_MAPPING.get(province, province),
            'AQI': aqi,
            'Date': datetime.now()
        })

    return pd.DataFrame(aqi_data)

def fetch_and_save_aqi():
    """Lấy dữ liệu AQI và lưu vào database"""
    # Lấy dữ liệu mới
    new_data = fetch_aqi()
    
    # Khởi tạo database
    db = AQIDatabase()
    
    # So sánh với dữ liệu cũ
    comparison = db.compare_aqi_data(new_data)
    
    # Lưu dữ liệu mới
    success = db.save_daily_aqi(new_data)
    
    if success:
        print("✅ Đã lưu dữ liệu AQI vào database")
        print(f"📊 Tổng số tỉnh: {comparison['summary']['total_provinces']}")
        print(f"🆕 Dữ liệu mới: {comparison['summary']['new_records_count']}")
        print(f"🔄 Dữ liệu cập nhật: {comparison['summary']['updated_records_count']}")
        print(f"➡️ Không thay đổi: {comparison['summary']['no_change_records_count']}")
        
        if comparison['summary']['avg_change'] != 0:
            print(f"📈 Thay đổi trung bình: {comparison['summary']['avg_change']:.2f}")
    else:
        print("❌ Lỗi khi lưu dữ liệu")
    
    return new_data, comparison

def get_aqi_comparison():
    """Lấy so sánh dữ liệu AQI"""
    db = AQIDatabase()
    latest_data = db.get_latest_aqi()
    comparison = db.compare_aqi_data(latest_data)
    return comparison

def get_aqi_trends(province: str = None, days: int = 7):
    """Lấy xu hướng AQI"""
    db = AQIDatabase()
    if province:
        return db.get_aqi_trends(province, days)
    else:
        # Lấy xu hướng cho tất cả tỉnh
        trends = {}
        for prov in config.PROVINCE_MAPPING.values():
            trends[prov] = db.get_aqi_trends(prov, days)
        return trends


# ✅ Test thủ công
if __name__ == '__main__':
    df = fetch_aqi()
    os.makedirs('data/raw', exist_ok=True)  # Tạo thư mục nếu chưa có
    df.to_csv('data/raw/initial_aqi.csv', index=False, encoding='utf-8-sig')
    print(df)
