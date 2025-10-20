import geopandas as gpd
import pandas as pd
import sqlite3
from backend.fetch_aqi import fetch_aqi
import config

def process_data():
    # Đọc shapefile
    provinces = gpd.read_file('data/raw/gadm41_VNM_1.shp')
    
    # Lấy AQI từ API hoặc CSV
    aqi_df = fetch_aqi()  # Hoặc pd.read_csv('data/raw/initial_aqi.csv')
    
    # Merge
    merged = provinces.merge(aqi_df, left_on='NAME_1', right_on='Province', how='left')
    merged['AQI'] = merged['AQI'].fillna(merged['AQI'].mean())
    
    # Lưu GeoJSON
    merged.to_file(config.DATA_PATH, driver='GeoJSON')
    
    # Lưu SQLite
    conn = sqlite3.connect(config.DB_PATH)
    aqi_df.to_sql('daily_aqi', conn, if_exists='append', index=False)
    conn.close()

if __name__ == '__main__':
    process_data()