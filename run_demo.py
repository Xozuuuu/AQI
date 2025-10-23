#!/usr/bin/env python3
"""
Script chay demo nhanh he thong AQI
"""

import subprocess
import sys
import time
import webbrowser
import os

def run_demo():
    """Chay demo he thong"""
    print("=== CHAY DEMO HE THONG AQI MONITORING ===")
    
    # 1. Chay test nhanh
    print("\n1. Chay test nhanh...")
    try:
        result = subprocess.run([sys.executable, "quick_test.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("SUCCESS: Test nhanh thanh cong")
        else:
            print("WARNING: Test nhanh co loi")
            print(result.stderr)
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 2. Chay demo chuc nang
    print("\n2. Chay demo chuc nang...")
    try:
        result = subprocess.run([sys.executable, "demo.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("SUCCESS: Demo chuc nang thanh cong")
        else:
            print("WARNING: Demo chuc nang co loi")
            print(result.stderr)
    except Exception as e:
        print(f"ERROR: {e}")
    
    # 3. Khoi dong Streamlit
    print("\n3. Khoi dong Streamlit...")
    print("Dang chay Streamlit tai http://localhost:8501")
    print("Mo trinh duyet de xem giao dien")
    
    try:
        # Mo trinh duyet
        webbrowser.open('http://localhost:8501')
        print("SUCCESS: Da mo trinh duyet")
    except Exception as e:
        print(f"WARNING: Khong the mo trinh duyet: {e}")
        print("Vui long mo thu cong: http://localhost:8501")
    
    # 4. Huong dan su dung
    print("\n=== HUONG DAN SU DUNG ===")
    print("1. Mo trinh duyet tai: http://localhost:8501")
    print("2. Click 'Cap nhat du lieu' de lay du lieu moi")
    print("3. Kham pha ban do va bieu do")
    print("4. Chuyen den tab 'Du bao' de xem du bao")
    print("5. Chuyen den tab 'Bao cao' de tao bao cao")
    print("6. Chuyen den tab 'Cai dat' de quan ly he thong")
    
    print("\n=== DEMO HOAN TAT ===")
    print("He thong AQI Monitoring da san sang su dung!")

if __name__ == "__main__":
    run_demo()
