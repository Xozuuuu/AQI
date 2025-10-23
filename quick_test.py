#!/usr/bin/env python3
"""
Quick test cho he thong AQI Monitoring
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Them duong dan de import cac module
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test import cac module"""
    print("Test import modules...")
    
    try:
        import streamlit as st
        print("SUCCESS: streamlit")
    except ImportError as e:
        print(f"ERROR: streamlit - {e}")
        return False
    
    try:
        import pandas as pd
        print("SUCCESS: pandas")
    except ImportError as e:
        print(f"ERROR: pandas - {e}")
        return False
    
    try:
        import numpy as np
        print("SUCCESS: numpy")
    except ImportError as e:
        print(f"ERROR: numpy - {e}")
        return False
    
    try:
        import plotly.express as px
        print("SUCCESS: plotly")
    except ImportError as e:
        print(f"ERROR: plotly - {e}")
        return False
    
    try:
        import folium
        print("SUCCESS: folium")
    except ImportError as e:
        print(f"ERROR: folium - {e}")
        return False
    
    try:
        import geopandas as gpd
        print("SUCCESS: geopandas")
    except ImportError as e:
        print(f"ERROR: geopandas - {e}")
        return False
    
    return True

def test_config():
    """Test config file"""
    print("\nTest config...")
    
    try:
        import config
        print(f"SUCCESS: API_KEY = {config.API_KEY[:10]}...")
        print(f"SUCCESS: So tinh = {len(config.PROVINCES_LIST)}")
        return True
    except Exception as e:
        print(f"ERROR: config - {e}")
        return False

def test_data_creation():
    """Test tao du lieu mau"""
    print("\nTest tao du lieu mau...")
    
    try:
        # Tao du lieu mau
        data = []
        provinces = ['Ha Noi', 'Ho Chi Minh City', 'Da Nang', 'Can Tho']
        
        for i in range(5):
            date = datetime.now() - timedelta(days=i)
            for province in provinces:
                data.append({
                    'Province': province,
                    'AQI': np.random.randint(20, 200),
                    'Date': date
                })
        
        df = pd.DataFrame(data)
        print(f"SUCCESS: Tao duoc {len(df)} ban ghi")
        print(f"   Cac tinh: {df['Province'].nunique()}")
        print(f"   AQI trung binh: {df['AQI'].mean():.1f}")
        
        # Luu vao file
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv('data/raw/test_aqi.csv', index=False, encoding='utf-8-sig')
        print("SUCCESS: Luu du lieu vao file")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_database():
    """Test database"""
    print("\nTest database...")
    
    try:
        import sqlite3
        
        # Tao database test
        os.makedirs('data/processed', exist_ok=True)
        conn = sqlite3.connect('data/processed/test_aqi.db')
        
        # Tao bang
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_aqi (
                id INTEGER PRIMARY KEY,
                Province TEXT,
                AQI INTEGER,
                Date TEXT
            )
        ''')
        
        # Them du lieu mau
        test_data = [
            ('Ha Noi', 85, '2024-01-15'),
            ('Ho Chi Minh City', 120, '2024-01-15'),
            ('Da Nang', 95, '2024-01-15')
        ]
        
        cursor.executemany('INSERT INTO test_aqi (Province, AQI, Date) VALUES (?, ?, ?)', test_data)
        conn.commit()
        
        # Doc du lieu
        df = pd.read_sql_query('SELECT * FROM test_aqi', conn)
        print(f"SUCCESS: Database co {len(df)} ban ghi")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Ham chinh"""
    print("QUICK TEST - He thong AQI Monitoring")
    print("=" * 50)
    
    tests = [
        ("Import modules", test_imports),
        ("Config", test_config),
        ("Tao du lieu", test_data_creation),
        ("Database", test_database)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"KET QUA: {passed}/{total} tests PASSED")
    
    if passed == total:
        print("SUCCESS: Tat ca tests deu PASSED!")
        print("He thong san sang hoat dong")
    else:
        print("ERROR: Mot so tests FAILED!")
        print("Vui long kiem tra va khac phuc loi")

if __name__ == "__main__":
    main()
