from apscheduler.schedulers.background import BackgroundScheduler
import logging
from backend.data_processing import process_data
from datetime import datetime
import time

# Cấu hình logging
logging.basicConfig(
    filename='logs/backend_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

def update_job():
    logging.info("BẮT ĐẦU chạy update_job()")  # Log bắt đầu
    try:
        process_data()
        logging.info(f"AQI updated successfully at {datetime.now()}")
    except Exception as e:
        logging.error(f"LỖI trong update_job: {e}", exc_info=True)

# Khởi tạo scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_job, 'cron', hour=8, minute=0)  # Chạy lúc 8h sáng
scheduler.start()

# GIỮ PROCESS SỐNG MÃI
if __name__ == '__main__':
    logging.info("Scheduler đã khởi động! Chạy job lúc 8h sáng.")
    print("Scheduler đang chạy... Nhấn Ctrl+C để dừng.")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler đang dừng...")
        scheduler.shutdown()
        print("Scheduler đã dừng.")