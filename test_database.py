#!/usr/bin/env python3
"""
Test script cho database AQI
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Them duong dan de import cac module
sys.path.append(os.path.dirname(__file__))

def test_database_creation():
    """Test tao database"""
    print("=== TEST: Tao database ===")
    
    try:
        from backend.database import AQIDatabase
        
        db = AQIDatabase()
        print("SUCCESS: Database da duoc tao")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_save_data():
    """Test luu du lieu"""
    print("\n=== TEST: Luu du lieu ===")
    
    try:
        from backend.database import AQIDatabase
        
        # Tao du lieu test
        test_data = pd.DataFrame({
            'Province': ['Ha Noi', 'Ho Chi Minh City', 'Da Nang'],
            'AQI': [85, 120, 95],
            'Date': [datetime.now().strftime('%Y-%m-%d')] * 3
        })
        
        db = AQIDatabase()
        success = db.save_daily_aqi(test_data)
        
        if success:
            print("SUCCESS: Luu du lieu thanh cong")
            return True
        else:
            print("ERROR: Luu du lieu that bai")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_comparison():
    """Test so sanh du lieu"""
    print("\n=== TEST: So sanh du lieu ===")
    
    try:
        from backend.database import AQIDatabase
        
        # Tao du lieu moi
        new_data = pd.DataFrame({
            'Province': ['Ha Noi', 'Ho Chi Minh City', 'Da Nang'],
            'AQI': [90, 125, 100],  # Thay doi so voi truoc
            'Date': [datetime.now().strftime('%Y-%m-%d')] * 3
        })
        
        db = AQIDatabase()
        comparison = db.compare_aqi_data(new_data)
        
        print(f"SUCCESS: So sanh du lieu")
        print(f"  - Tong tinh: {comparison['summary']['total_provinces']}")
        print(f"  - Du lieu moi: {comparison['summary']['new_records_count']}")
        print(f"  - Du lieu cap nhat: {comparison['summary']['updated_records_count']}")
        print(f"  - Khong thay doi: {comparison['summary']['no_change_records_count']}")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_trends():
    """Test phan tich xu huong"""
    print("\n=== TEST: Phan tich xu huong ===")
    
    try:
        from backend.database import AQIDatabase
        
        # Tao du lieu lich su
        historical_data = []
        provinces = ['Ha Noi', 'Ho Chi Minh City', 'Da Nang']
        
        for i in range(7):  # 7 ngay
            date = datetime.now() - timedelta(days=i)
            for province in provinces:
                historical_data.append({
                    'Province': province,
                    'AQI': 80 + i * 5 + np.random.randint(-10, 10),  # Xu huong tang
                    'Date': date.strftime('%Y-%m-%d')
                })
        
        df = pd.DataFrame(historical_data)
        
        db = AQIDatabase()
        db.save_daily_aqi(df)
        
        # Test xu huong
        trends = db.get_aqi_trends('Ha Noi', 7)
        print(f"SUCCESS: Phan tich xu huong")
        print(f"  - Xu huong: {trends['trend']}")
        print(f"  - Huong: {trends['direction']}")
        print(f"  - Ty le thay doi: {trends['change_rate']}%")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_ranking():
    """Test xep hang tinh"""
    print("\n=== TEST: Xep hang tinh ===")
    
    try:
        from backend.database import AQIDatabase
        
        db = AQIDatabase()
        ranking = db.get_province_ranking()
        
        if not ranking.empty:
            print("SUCCESS: Xep hang tinh")
            print("Top 5 tinh co AQI tot nhat:")
            for i, row in ranking.head(5).iterrows():
                print(f"  {i+1}. {row['province']}: {row['aqi']}")
        else:
            print("WARNING: Khong co du lieu de xep hang")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_statistics():
    """Test thong ke"""
    print("\n=== TEST: Thong ke ===")
    
    try:
        from backend.database import AQIDatabase
        
        db = AQIDatabase()
        stats = db.get_aqi_statistics(days=7)
        
        if stats:
            print("SUCCESS: Thong ke")
            print(f"  - So tinh co du lieu: {len(stats)}")
            for stat in stats[:3]:  # Hien thi 3 tinh dau
                print(f"  - {stat['province']}: Min={stat['min_aqi']}, Max={stat['max_aqi']}, Avg={stat['avg_aqi']:.1f}")
        else:
            print("WARNING: Khong co du lieu thong ke")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Ham chinh"""
    print("TEST DATABASE AQI MONITORING")
    print("=" * 50)
    
    tests = [
        ("Tao database", test_database_creation),
        ("Luu du lieu", test_save_data),
        ("So sanh du lieu", test_comparison),
        ("Phan tich xu huong", test_trends),
        ("Xep hang tinh", test_ranking),
        ("Thong ke", test_statistics)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"KET QUA TEST: {passed}/{total} thanh cong")
    
    if passed == total:
        print("SUCCESS: Tat ca tests deu thanh cong!")
        print("Database san sang su dung")
    else:
        print("WARNING: Mot so tests that bai")
        print("Kiem tra lai cac thanh phan")

if __name__ == "__main__":
    main()
