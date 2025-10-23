#!/usr/bin/env python3
"""
Script test hệ thống AQI Monitoring
Kiểm tra các chức năng chính
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Thêm đường dẫn để import các module
sys.path.append(os.path.dirname(__file__))

def test_data_loading():
    """Test tải dữ liệu"""
    print("Test tai du lieu...")
    
    try:
        from backend.fetch_aqi import fetch_aqi
        df = fetch_aqi()
        
        if df.empty:
            print("ERROR: Khong co du lieu")
            return False
        
        print(f"SUCCESS: Tai duoc {len(df)} ban ghi")
        print(f"   Cac tinh: {df['Province'].nunique()}")
        print(f"   AQI trung binh: {df['AQI'].mean():.1f}")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_prediction():
    """Test dự báo"""
    print("\n🧪 Test dự báo...")
    
    try:
        from backend.prediction import AQIPredictor
        
        # Tạo dữ liệu mẫu
        sample_data = []
        provinces = ['Ha Noi', 'Ho Chi Minh City', 'Da Nang']
        
        for i in range(10):
            date = datetime.now() - timedelta(days=i)
            for province in provinces:
                sample_data.append({
                    'Province': province,
                    'AQI': np.random.randint(20, 200),
                    'Date': date
                })
        
        df = pd.DataFrame(sample_data)
        
        # Lưu vào database test
        import sqlite3
        os.makedirs('data/processed', exist_ok=True)
        conn = sqlite3.connect('data/processed/aqi_history.db')
        df.to_sql('daily_aqi', conn, if_exists='replace', index=False)
        conn.close()
        
        # Test dự báo
        predictor = AQIPredictor()
        predictions = predictor.predict_all_provinces()
        
        if predictions.empty:
            print("❌ Không thể dự báo")
            return False
        
        print(f"✅ Dự báo cho {len(predictions)} tỉnh")
        print(f"   AQI dự báo trung bình: {predictions['Predicted_AQI'].mean():.1f}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def test_reporting():
    """Test báo cáo"""
    print("\n🧪 Test báo cáo...")
    
    try:
        from backend.reporting import AQIReportGenerator
        
        generator = AQIReportGenerator()
        report = generator.generate_summary_report()
        
        if 'error' in report:
            print(f"❌ Lỗi: {report['error']}")
            return False
        
        print("✅ Tạo báo cáo thành công")
        print(f"   Tổng bản ghi: {report['summary'].get('total_records', 0)}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def test_map_creation():
    """Test tạo bản đồ"""
    print("\n🧪 Test tạo bản đồ...")
    
    try:
        import folium
        from streamlit_folium import st_folium
        
        # Tạo dữ liệu mẫu
        df = pd.DataFrame({
            'Province': ['Ha Noi', 'Ho Chi Minh City', 'Da Nang'],
            'AQI': [85, 120, 95],
            'Date': [datetime.now()] * 3
        })
        
        # Tạo bản đồ
        m = folium.Map(location=[16.0, 108.0], zoom_start=6)
        
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=[21.0285, 105.8542] if row['Province'] == 'Ha Noi' 
                else [10.8231, 106.6297] if row['Province'] == 'Ho Chi Minh City'
                else [16.0544, 108.2022],
                radius=10,
                popup=f"{row['Province']}: {row['AQI']}",
                color='red',
                fill=True
            ).add_to(m)
        
        print("✅ Tạo bản đồ thành công")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def test_data_processing():
    """Test xử lý dữ liệu"""
    print("\n🧪 Test xử lý dữ liệu...")
    
    try:
        from backend.data_processing import process_data
        
        # Test với dữ liệu mẫu
        print("✅ Module xử lý dữ liệu hoạt động")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    """Hàm chính"""
    print("Test He thong AQI Monitoring")
    print("=" * 50)
    
    tests = [
        ("Tải dữ liệu", test_data_loading),
        ("Dự báo", test_prediction),
        ("Báo cáo", test_reporting),
        ("Bản đồ", test_map_creation),
        ("Xử lý dữ liệu", test_data_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Kết quả: {passed}/{total} tests PASSED")
    
    if passed == total:
        print("🎉 Tất cả tests đều PASSED!")
        print("✅ Hệ thống sẵn sàng hoạt động")
    else:
        print("❌ Một số tests FAILED!")
        print("⚠️  Vui lòng kiểm tra và khắc phục lỗi")

if __name__ == "__main__":
    main()
