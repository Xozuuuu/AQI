import requests
import pandas as pd
from datetime import datetime
import sys
import os
from decouple import config  # ✅ Dùng để đọc .env

# ✅ Lấy đường dẫn gốc dự án từ .env
project_root = config('PROJECT_ROOT')
sys.path.append(os.path.normpath(project_root))  # Đảm bảo path không lỗi dù có dấu cách

import config  # Import cấu hình sau khi thêm project_root vào path


def fetch_aqi():
    aqi_data = []
    for province in config.PROVINCES_LIST:
        url = f'https://api.waqi.info/feed/{province}/?token={config.API_KEY}'
        response = requests.get(url).json()
        print("Response for", province, ":", response)  # Debug

        if response.get('status') == 'ok' and isinstance(response.get('data'), dict):
            aqi = response['data'].get('aqi')
            if aqi in ('-', None, ''):
                aqi = None
                print(f"Cảnh báo: AQI thiếu cho {province}.")
        else:
            aqi = None

        aqi_data.append({
            'Province': config.PROVINCE_MAPPING.get(province, province),
            'AQI': aqi,
            'Date': datetime.now()
        })

    return pd.DataFrame(aqi_data)


# ✅ Test thủ công
if __name__ == '__main__':
    df = fetch_aqi()
    os.makedirs('data/raw', exist_ok=True)  # Tạo thư mục nếu chưa có
    df.to_csv('data/raw/initial_aqi.csv', index=False, encoding='utf-8-sig')
    print(df)
