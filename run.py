import sys
import os
import pandas as pd

# Thêm đường dẫn để import các module nội bộ
sys.path.append(os.path.dirname(__file__))

from backend.fetch_aqi import fetch_aqi
import config

def main():
    print("=== Bắt đầu lấy dữ liệu AQI ===")
    df = fetch_aqi()  # ✅ Gọi đúng

    # Hiển thị kết quả
    print("\nDữ liệu thu thập được:")
    print(df)

    # Tạo thư mục lưu dữ liệu nếu chưa có
    os.makedirs('data/raw', exist_ok=True)

    # Lưu kết quả ra file CSV
    output_path = 'data/raw/latest_aqi.csv'
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"\n✅ Đã lưu dữ liệu thành công vào: {output_path}")

if __name__ == "__main__":
    main()
