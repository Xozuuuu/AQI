#!/usr/bin/env python3
"""
Script khởi động hệ thống AQI Monitoring
Kiểm tra dependencies và cấu hình trước khi chạy
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên")
        print(f"   Phiên bản hiện tại: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Kiểm tra các thư viện cần thiết"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'plotly',
        'folium',
        'geopandas',
        'requests',
        'sklearn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                import sklearn
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Thiếu các thư viện: {', '.join(missing_packages)}")
        print("   Chạy: pip install -r docs/requirements.txt")
        return False
    
    return True

def check_config():
    """Kiểm tra file cấu hình"""
    config_files = [
        'config.py',
        '.streamlit/config.toml',
        'env.example'
    ]
    
    for file in config_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            return False
    
    return True

def check_data_directories():
    """Tạo thư mục dữ liệu nếu chưa có"""
    directories = [
        'data',
        'data/raw',
        'data/processed',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}/")
    
    return True

def check_api_key():
    """Kiểm tra API key"""
    try:
        import config
        if hasattr(config, 'API_KEY') and config.API_KEY:
            print(f"✅ API Key: {config.API_KEY[:10]}...")
            return True
        else:
            print("⚠️  API Key chưa được cấu hình")
            return False
    except Exception as e:
        print(f"❌ Lỗi đọc config: {e}")
        return False

def main():
    """Hàm chính"""
    print("🌍 Kiểm tra Hệ thống AQI Monitoring")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Configuration", check_config),
        ("Data Directories", check_data_directories),
        ("API Key", check_api_key)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 Tất cả kiểm tra đều PASSED!")
        print("🚀 Đang khởi động ứng dụng...")
        
        # Chạy Streamlit
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", "app.py",
                "--server.port=8501",
                "--server.address=0.0.0.0"
            ])
        except KeyboardInterrupt:
            print("\n👋 Tạm biệt!")
        except Exception as e:
            print(f"❌ Lỗi khởi động: {e}")
    else:
        print("❌ Có lỗi trong quá trình kiểm tra!")
        print("   Vui lòng khắc phục các lỗi trên trước khi chạy lại.")
        sys.exit(1)

if __name__ == "__main__":
    main()
