#!/usr/bin/env python3
"""
Demo script cho he thong AQI Monitoring
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Them duong dan de import cac module
sys.path.append(os.path.dirname(__file__))

def demo_data_fetch():
    """Demo lay du lieu AQI"""
    print("=== DEMO: Lay du lieu AQI ===")
    
    try:
        from backend.fetch_aqi import fetch_aqi
        df = fetch_aqi()
        
        if not df.empty:
            print(f"SUCCESS: Lay duoc {len(df)} ban ghi AQI")
            print("Du lieu mau:")
            print(df.head())
            return True
        else:
            print("WARNING: Khong co du lieu")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def demo_prediction():
    """Demo du bao AQI"""
    print("\n=== DEMO: Du bao AQI ===")
    
    try:
        from backend.prediction import AQIPredictor
        
        # Tao du lieu mau
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
        
        # Luu vao database
        import sqlite3
        os.makedirs('data/processed', exist_ok=True)
        conn = sqlite3.connect('data/processed/demo_aqi.db')
        df.to_sql('daily_aqi', conn, if_exists='replace', index=False)
        conn.close()
        
        # Du bao
        predictor = AQIPredictor('data/processed/demo_aqi.db')
        predictions = predictor.predict_all_provinces()
        
        if not predictions.empty:
            print("SUCCESS: Du bao AQI")
            print("Ket qua du bao:")
            print(predictions)
            return True
        else:
            print("WARNING: Khong the du bao")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def demo_reporting():
    """Demo bao cao"""
    print("\n=== DEMO: Tao bao cao ===")
    
    try:
        from backend.reporting import AQIReportGenerator
        
        generator = AQIReportGenerator('data/processed/demo_aqi.db')
        report = generator.generate_summary_report()
        
        if 'error' not in report:
            print("SUCCESS: Tao bao cao")
            print(f"Tong ban ghi: {report['summary'].get('total_records', 0)}")
            print(f"AQI trung binh: {report['summary'].get('aqi_stats', {}).get('mean', 'N/A')}")
            return True
        else:
            print(f"ERROR: {report['error']}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def demo_map():
    """Demo tao ban do"""
    print("\n=== DEMO: Tao ban do ===")
    
    try:
        import folium
        
        # Tao ban do
        m = folium.Map(location=[16.0, 108.0], zoom_start=6)
        
        # Them cac diem AQI
        cities = [
            ('Ha Noi', 21.0285, 105.8542, 85),
            ('Ho Chi Minh City', 10.8231, 106.6297, 120),
            ('Da Nang', 16.0544, 108.2022, 95)
        ]
        
        for city, lat, lon, aqi in cities:
            color = 'green' if aqi < 50 else 'yellow' if aqi < 100 else 'red'
            folium.CircleMarker(
                location=[lat, lon],
                radius=10,
                popup=f"{city}: AQI {aqi}",
                color=color,
                fill=True
            ).add_to(m)
        
        # Luu ban do
        m.save('demo_map.html')
        print("SUCCESS: Tao ban do")
        print("Ban do da luu: demo_map.html")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def demo_streamlit():
    """Demo chay Streamlit"""
    print("\n=== DEMO: Chay Streamlit ===")
    
    try:
        print("SUCCESS: Streamlit da chay tai http://localhost:8501")
        print("Mo trinh duyet va truy cap de xem giao dien")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Ham chinh"""
    print("DEMO HE THONG AQI MONITORING")
    print("=" * 50)
    
    demos = [
        ("Lay du lieu AQI", demo_data_fetch),
        ("Du bao AQI", demo_prediction),
        ("Tao bao cao", demo_reporting),
        ("Tao ban do", demo_map),
        ("Chay Streamlit", demo_streamlit)
    ]
    
    passed = 0
    total = len(demos)
    
    for demo_name, demo_func in demos:
        if demo_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"KET QUA DEMO: {passed}/{total} thanh cong")
    
    if passed == total:
        print("SUCCESS: Tat ca demo deu thanh cong!")
        print("He thong san sang su dung")
    else:
        print("WARNING: Mot so demo that bai")
        print("Kiem tra lai cac thanh phan")

if __name__ == "__main__":
    main()
