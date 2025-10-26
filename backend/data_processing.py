# backend/data_processing.py
import geopandas as gpd
import pandas as pd
import sqlite3
from backend.fetch_aqi import fetch_aqi
import config
from datetime import datetime

def process_data():
    # 1. Đọc shapefile 63 tỉnh
    gdf = gpd.read_file('data/raw/gadm41_VNM_1.shp')
    
    # 2. Lấy AQI từ API (aqi_df đã chứa tên tiếng Việt)
    aqi_df = fetch_aqi()
    
    # 3. Chuẩn bị merge:
    # aqi_df['Province'] đã chứa tên tiếng Việt (vd: 'Hà Nội')
    # Chúng ta chỉ cần tạo dict: {'Hà Nội': 50, 'Thái Nguyên': 60}
    province_aqi = dict(zip(
        aqi_df['Province'],
        aqi_df['AQI']
    ))
    
    # 4. GÁN AQI CHO TỈNH TRONG SHAPEFILE
    gdf = gdf.copy()
    # Gán AQI dựa trên tên tiếng Việt khớp giữa 'NAME_1' và 'province_aqi'
    gdf['AQI'] = gdf['NAME_1'].map(province_aqi) 
    gdf['AQI'] = pd.to_numeric(gdf['AQI'], errors='coerce')
    
    # 5. LỌC RA CÁC TỈNH CÓ DỮ LIỆU
    # Bỏ tất cả các hàng (tỉnh) không có dữ liệu AQI
    # gdf = gdf.dropna(subset=['AQI'])
    
    # 6. XỬ LÝ NGÀY
    if 'Date' in aqi_df.columns and not aqi_df.empty:
        valid_dates = aqi_df['Date'].dropna()
        if not valid_dates.empty:
            update_time = pd.to_datetime(valid_dates.iloc[0]).strftime('%Y-%m-%d %H:%M')
        else:
            update_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    else:
        update_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
    gdf['Date'] = update_time
    
    # 7. LƯU GeoJSON (Chỉ còn các tỉnh có AQI)
    gdf.to_file(config.DATA_PATH, driver='GeoJSON')
    
    # 8. LƯU DB
    conn = sqlite3.connect(config.DB_PATH)
    aqi_df.to_sql('daily_aqi', conn, if_exists='append', index=False)
    conn.close()
    
    # 9. IN LOG (Cập nhật log)
    print(f"XỬ LÝ HOÀN TẤT!")
    print(f"   Đã lọc và chỉ lưu {len(gdf)} tỉnh có dữ liệu AQI.")
    print(f"   GeoJSON đã được cập nhật tại: {config.DATA_PATH}")
    print(f"   Dữ liệu thô đã được lưu vào DB: {config.DB_PATH}")

if __name__ == '__main__':
    process_data()