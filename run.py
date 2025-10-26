# run.py - Chạy Scheduler + Streamlit cùng lúc (không block)

import subprocess
import threading
import time
import os
import sys  # <-- 1. IMPORT SYS

# Đảm bảo thư mục logs
os.makedirs("logs", exist_ok=True)

def start_scheduler():
    print("Starting AQI Scheduler (8:00 AM daily)...")
    subprocess.Popen([
        sys.executable, "-m", "backend.scheduler"  # <-- 2. USE SYS.EXECUTABLE
    ], creationflags=subprocess.CREATE_NEW_CONSOLE) # Mở cửa sổ mới

def start_streamlit():
    print("Starting Streamlit Dashboard at http://localhost:8501 ...")
    subprocess.Popen([
        sys.executable, "-m", "streamlit", "run", "frontend/app.py", # <-- 3. USE SYS.EXECUTABLE
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ], creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == '__main__':
    # Bắt đầu scheduler
    scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
    scheduler_thread.start()

    time.sleep(3) # Đợi scheduler khởi động

    # Bắt đầu Streamlit
    start_streamlit()

    print("\nCẢ 2 ĐÃ CHẠY!")
    print("→ Scheduler: nền, cập nhật 8h sáng")
    print("→ Dashboard: http://localhost:8501")
    print("→ Nhấn Ctrl+C để dừng run.py")

    # Giữ run.py chạy mãi
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDừng run.py...")