#!/usr/bin/env python3
"""
Setup script cho he thong AQI Monitoring
"""

import os
import sys
import subprocess
import platform

def check_python():
    """Kiem tra Python version"""
    print("Kiem tra Python...")
    if sys.version_info < (3, 8):
        print("ERROR: Can Python 3.8 tro len")
        return False
    print(f"SUCCESS: Python {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Cai dat dependencies"""
    print("\nCai dat dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "docs/requirements.txt"], 
                      check=True)
        print("SUCCESS: Cai dat dependencies thanh cong")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Cai dat dependencies that bai: {e}")
        return False

def create_directories():
    """Tao thu muc can thiet"""
    print("\nTao thu muc...")
    directories = [
        'data',
        'data/raw',
        'data/processed',
        'logs',
        '.streamlit'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"SUCCESS: {directory}/")
    
    return True

def create_config_files():
    """Tao file cau hinh"""
    print("\nTao file cau hinh...")
    
    # Tao .env tu env.example
    if not os.path.exists('.env') and os.path.exists('env.example'):
        import shutil
        shutil.copy('env.example', '.env')
        print("SUCCESS: Tao file .env")
    
    # Tao secrets.toml
    secrets_file = '.streamlit/secrets.toml'
    if not os.path.exists(secrets_file):
        with open(secrets_file, 'w', encoding='utf-8') as f:
            f.write('''# Streamlit secrets configuration
[api]
api_key = "your_aqi_api_key_here"

[database]
host = "localhost"
port = 5432
name = "aqi_monitoring"
user = "aqi_user"
password = "aqi_password"
''')
        print("SUCCESS: Tao file secrets.toml")
    
    return True

def run_tests():
    """Chay tests"""
    print("\nChay tests...")
    try:
        result = subprocess.run([sys.executable, "quick_test.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("SUCCESS: Tests thanh cong")
            return True
        else:
            print("WARNING: Tests co loi")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Ham chinh"""
    print("=== SETUP HE THONG AQI MONITORING ===")
    
    steps = [
        ("Kiem tra Python", check_python),
        ("Cai dat dependencies", install_dependencies),
        ("Tao thu muc", create_directories),
        ("Tao file cau hinh", create_config_files),
        ("Chay tests", run_tests)
    ]
    
    passed = 0
    total = len(steps)
    
    for step_name, step_func in steps:
        print(f"\n{step_name}:")
        if step_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"KET QUA SETUP: {passed}/{total} thanh cong")
    
    if passed == total:
        print("SUCCESS: Setup hoan tat!")
        print("\n=== HUONG DAN SU DUNG ===")
        print("1. Chay ung dung: streamlit run app.py")
        print("2. Hoac: python start.py")
        print("3. Hoac: python run_demo.py")
        print("4. Mo trinh duyet: http://localhost:8501")
    else:
        print("WARNING: Setup co loi!")
        print("Vui long kiem tra va khac phuc")

if __name__ == "__main__":
    main()
