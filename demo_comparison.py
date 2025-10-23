#!/usr/bin/env python3
"""
Demo script cho tinh nang so sanh du lieu AQI
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Them duong dan de import cac module
sys.path.append(os.path.dirname(__file__))

def demo_data_comparison():
    """Demo so sanh du lieu"""
    print("=== DEMO: So sanh du lieu AQI ===")
    
    try:
        from backend.database import AQIDatabase
        from backend.fetch_aqi import fetch_and_save_aqi
        
        # Tao du lieu mau
        print("1. Tao du lieu mau...")
        
        # Du lieu ngay hom qua
        yesterday_data = []
        provinces = ['Ha Noi', 'Ho Chi Minh City', 'Da Nang', 'Can Tho', 'Hai Phong']
        
        for province in provinces:
            yesterday_data.append({
                'Province': province,
                'AQI': np.random.randint(50, 150),
                'Date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            })
        
        df_yesterday = pd.DataFrame(yesterday_data)
        
        # Luu du lieu hom qua
        db = AQIDatabase()
        db.save_daily_aqi(df_yesterday)
        print(f"   SUCCESS: Da luu du lieu hom qua cho {len(provinces)} tinh")
        
        # Du lieu ngay hom nay (co thay doi)
        print("2. Tao du lieu hom nay...")
        
        today_data = []
        for i, province in enumerate(provinces):
            # Tao thay doi ngau nhien
            change = np.random.randint(-20, 30)
            new_aqi = max(0, yesterday_data[i]['AQI'] + change)
            
            today_data.append({
                'Province': province,
                'AQI': new_aqi,
                'Date': datetime.now().strftime('%Y-%m-%d')
            })
        
        df_today = pd.DataFrame(today_data)
        
        # So sanh du lieu
        print("3. So sanh du lieu...")
        comparison = db.compare_aqi_data(df_today)
        
        print(f"   SUCCESS: So sanh hoan tat")
        print(f"   - Tong tinh: {comparison['summary']['total_provinces']}")
        print(f"   - Du lieu moi: {comparison['summary']['new_records_count']}")
        print(f"   - Du lieu cap nhat: {comparison['summary']['updated_records_count']}")
        print(f"   - Khong thay doi: {comparison['summary']['no_change_records_count']}")
        
        # Hien thi chi tiet thay doi
        if comparison['updated_records']:
            print("\n4. Chi tiet thay doi:")
            for record in comparison['updated_records']:
                change = record['change']
                change_pct = record['change_percentage']
                print(f"   - {record['province']}: {record['old_aqi']} -> {record['new_aqi']} ({change:+.1f}, {change_pct:+.1f}%)")
        
        # Luu du lieu hom nay
        print("5. Luu du lieu hom nay...")
        db.save_daily_aqi(df_today)
        print("   SUCCESS: Da luu du lieu hom nay")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def demo_trend_analysis():
    """Demo phan tich xu huong"""
    print("\n=== DEMO: Phan tich xu huong ===")
    
    try:
        from backend.database import AQIDatabase
        
        # Tao du lieu lich su 7 ngay
        print("1. Tao du lieu lich su 7 ngay...")
        
        historical_data = []
        provinces = ['Ha Noi', 'Ho Chi Minh City', 'Da Nang']
        
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            for j, province in enumerate(provinces):
                # Tao xu huong khac nhau cho moi tinh
                if province == 'Ha Noi':
                    aqi = 80 + i * 3 + np.random.randint(-5, 5)  # Xu huong tang nhe
                elif province == 'Ho Chi Minh City':
                    aqi = 120 - i * 2 + np.random.randint(-5, 5)  # Xu huong giam
                else:  # Da Nang
                    aqi = 95 + np.random.randint(-10, 10)  # On dinh
                
                historical_data.append({
                    'Province': province,
                    'AQI': max(0, int(aqi)),
                    'Date': date.strftime('%Y-%m-%d')
                })
        
        df_historical = pd.DataFrame(historical_data)
        
        # Luu du lieu lich su
        db = AQIDatabase()
        db.save_daily_aqi(df_historical)
        print(f"   SUCCESS: Da luu du lieu lich su cho {len(provinces)} tinh")
        
        # Phan tich xu huong
        print("2. Phan tich xu huong...")
        
        for province in provinces:
            trend = db.get_aqi_trends(province, 7)
            print(f"   - {province}:")
            print(f"     + Xu huong: {trend['trend']}")
            print(f"     + Huong: {trend['direction']}")
            print(f"     + Ty le thay doi: {trend['change_rate']}%")
            print(f"     + Diem du lieu: {trend['data_points']}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def demo_ranking():
    """Demo xep hang tinh"""
    print("\n=== DEMO: Xep hang tinh ===")
    
    try:
        from backend.database import AQIDatabase
        
        db = AQIDatabase()
        ranking = db.get_province_ranking()
        
        if not ranking.empty:
            print("SUCCESS: Xep hang tinh theo AQI")
            print("Top 10 tinh co AQI tot nhat:")
            
            for i, row in ranking.head(10).iterrows():
                aqi = row['aqi']
                if aqi <= 50:
                    status = "TOT"
                elif aqi <= 100:
                    status = "TRUNG BINH"
                elif aqi <= 150:
                    status = "KHONG TOT"
                else:
                    status = "XAU"
                
                print(f"   {i+1:2d}. {row['province']:20s}: {aqi:3d} ({status})")
        else:
            print("WARNING: Khong co du lieu de xep hang")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def demo_statistics():
    """Demo thong ke"""
    print("\n=== DEMO: Thong ke AQI ===")
    
    try:
        from backend.database import AQIDatabase
        
        db = AQIDatabase()
        stats = db.get_aqi_statistics(days=7)
        
        if stats:
            print("SUCCESS: Thong ke AQI 7 ngay qua")
            print("Chi tiet theo tinh:")
            
            for stat in stats:
                province = stat['province']
                min_aqi = stat['min_aqi']
                max_aqi = stat['max_aqi']
                avg_aqi = stat['avg_aqi']
                total_records = stat['total_records']
                
                print(f"   - {province}:")
                print(f"     + Min: {min_aqi}, Max: {max_aqi}, Trung binh: {avg_aqi:.1f}")
                print(f"     + So ban ghi: {total_records}")
        else:
            print("WARNING: Khong co du lieu thong ke")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Ham chinh"""
    print("DEMO TINH NANG SO SANH DU LIEU AQI")
    print("=" * 60)
    
    demos = [
        ("So sanh du lieu", demo_data_comparison),
        ("Phan tich xu huong", demo_trend_analysis),
        ("Xep hang tinh", demo_ranking),
        ("Thong ke", demo_statistics)
    ]
    
    passed = 0
    total = len(demos)
    
    for demo_name, demo_func in demos:
        if demo_func():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"KET QUA DEMO: {passed}/{total} thanh cong")
    
    if passed == total:
        print("SUCCESS: Tat ca demo deu thanh cong!")
        print("Tinh nang so sanh du lieu san sang su dung")
    else:
        print("WARNING: Mot so demo that bai")
        print("Kiem tra lai cac thanh phan")

if __name__ == "__main__":
    main()
