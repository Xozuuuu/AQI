# frontend/app.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from streamlit_folium import st_folium
from frontend.visualize import create_map
import geopandas as gpd
import config
import pandas as pd
import urllib.parse # Thư viện để mã hóa URL (quan trọng)
from textwrap import dedent

@st.cache_data(ttl=3600)  # Cache 1 giờ
def load_data():
    gdf = gpd.read_file(config.DATA_PATH)
    gdf['AQI'] = pd.to_numeric(gdf['AQI'], errors='coerce')
    return gdf

gdf = load_data()  # DÙNG CHUNG CHO TOÀN BỘ APP
# =================================================================
# 1. CẤU HÌNH TRANG
# =================================================================
st.set_page_config(page_title="AirWatch VN", layout="wide")

# =================================================================
# 2. CSS (ĐÃ SỬA LẠI)
# =================================================================
st.markdown("""
<style>
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}
[data-testid="stHeader"], footer { display: none; }
iframe { 
    height: 800px !important; 
    border-radius: 12px !important; 
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

/* CSS CHO TIÊU ĐỀ SIDEBAR (MỚI) */
.sidebar-title-box {
    background-color: #1a1a1a;
    border: 1px solid #404040;
    border-radius: 8px;
    padding: 10px 16px; /* Căn lề cho chữ */
    margin-bottom: 6px; /* Khoảng cách với list bên dưới */
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    /* Set chiều cao cố định để ngang bằng nút "Cập nhật" */
    height: 40px; 
    display: flex;
    align-items: center;
    justify-content: center;
}
.sidebar-title-box h3 {
    color: white;
    margin: 0; /* Xóa margin mặc định của h3 */
    font-size: 1.25rem; /* Cỡ chữ */
}

/* CSS CHO DANH SÁCH CUỘN (SCROLLBAR) */
.right-sidebar-list {
    /* Chiều cao 800px (chiều cao bản đồ) TRỪ đi chiều cao title (55px + 6px margin) */
    margin-top :10px;
    height: 800px !important; 
    max-height: 800px !important;
    overflow-y: auto !important; 
    overflow-x: hidden !important;
    background-color: #1a1a1a !important;
    border-radius: 12px !important;
    padding: 16px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
}

/* Style cho các link <a> (thay cho st.button) */
.province-item {
    /* ... (CSS cho .province-item, .province-item:hover, .aqi-highlight giữ nguyên) ... */
    width: 100%;
    padding: 12px;
    margin: 6px 0;
    background: #2a2a2a;
    border: 1px solid #404040;
    border-radius: 8px;
    color: white;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s;
    display: block; 
}

.right-sidebar-list a {
    text-decoration: none;
}

.province-item:hover {
    background: #3a3a3a;
    border-color: #505050;
    transform: translateX(4px);
    color: white; 
}
.aqi-highlight {
    font-weight: bold;
    font-size: 16px;
    float: right; 
}

.bg-img {
    margin-top: 24px;
    width: 100%;
    height: 400px;
    background-origin : border-box;
    border-radius: 16px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    color: white;
    border : 2px solid white;
    padding: 40px 50px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    font-family: 'Segoe UI', sans-serif;
    position: relative;
    overflow: hidden;
}  
                  
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. LAYOUT: TIÊU ĐỀ CHUNG VÀ 2 CỘT
# =================================================================
# ĐƯA TIÊU ĐỀ RA NGOÀI ĐỂ NÓ FULL-WIDTH
st.title("AirWatch – Giám sát chất lượng không khí Việt Nam")

col1, col2 = st.columns([3, 1])

with col1:
    # NÚT CẬP NHẬT (SẼ NGANG HÀNG VỚI TITLE SIDEBAR)
    if st.button("Cập nhật dữ liệu AQI", type="primary", use_container_width=True):
        with st.spinner("Đang lấy dữ liệu mới..."):
            try:
                from backend.data_processing import process_data
                process_data()
                st.success("✅ Cập nhật thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")

    # Xử lý state của bản đồ
    if 'selected_province' not in st.session_state:
        st.session_state.selected_province = None
    
    if "province" in st.query_params:
        clicked_province = urllib.parse.unquote(st.query_params["province"])
        
        if clicked_province == "None":
            st.session_state.selected_province = None
        else:
            st.session_state.selected_province = clicked_province
        
        st.query_params.clear()
    
    # BẢN ĐỒ
    m = create_map(st.session_state.selected_province)
    st_folium(m, width=None, height=800, returned_objects=[])

    #========================================================
    # =================================================================
with col2:
    # ===== SỬA LỖI TẠI ĐÂY =====
    
    # 1. HIỂN THỊ TITLE BAR (RIÊNG BIỆT)
    # Đây là phần sẽ ngang hàng với nút "Cập nhật"
    st.markdown('<div class="sidebar-title-box"><h3>Danh sách tỉnh</h3></div>', unsafe_allow_html=True)
    
    # 2. HIỂN THỊ DANH SÁCH CUỘN (SCROLLBAR)
    
    # Đọc và lọc dữ liệu
    # gdf = gpd.read_file(config.DATA_PATH)
    # gdf['AQI'] = pd.to_numeric(gdf['AQI'], errors='coerce')
    # provinces = gdf.sort_values('AQI', ascending=False).dropna(subset=['AQI'])
    provinces = gdf.sort_values('AQI', ascending=False).dropna(subset=['AQI'])
    
    # Bắt đầu xây dựng chuỗi HTML (cho phần list)
    # Dùng class mới: .right-sidebar-list
    html_list_content = '<div class="right-sidebar-list">'
    
    for _, row in provinces.iterrows():
        province = row['NAME_1']
        aqi = row['AQI']
        
        aqi_str = f"{int(aqi)}"
        if aqi <= 50:
            color = "#00e400"
        elif aqi <= 100:
            color = "#ffff00" # Sửa thành vàng chuẩn
        elif aqi <= 150:
            color = "#ff7e00"
        elif aqi <= 200:
            color = "#ff0000"
        else:
            color = "#99004c"
        
        province_url_encoded = urllib.parse.quote(province)
        
        # Tránh thụt lề 4+ spaces trong Markdown (bị hiển thị như code block)
        html_list_content += dedent(f"""
        <a href="?province={province_url_encoded}" target="_self" class="province-item">
            {province}
            <span class='aqi-highlight' style='color: {color};'>{aqi_str}</span>
        </a>
        """)
    
    html_list_content += f'<hr><a href="?province=None" target="_self" class="province-item" style="text-align: center;">🗑️ Ẩn đánh dấu</a>'
    html_list_content += '</div>'
    
    # Hiển thị list bằng 1 lệnh st.markdown
    st.markdown(html_list_content, unsafe_allow_html=True)

# =========================================================

# =================================================================
# THANH THÔNG TIN – DÙNG ẢNH LOCAL (giữ nguyên mọi thứ bạn đang có)
# =================================================================
import base64
from pathlib import Path

# Hàm nhúng ảnh local thành base64 (không cần server)
def img_to_base64(img_path):
    if img_path.exists():
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# Thư mục ảnh tỉnh
IMG_DIR = Path(__file__).parent / "static" / "province"

# Mapping tên tỉnh → tên file ảnh (không dấu, chữ thường)
PROVINCE_IMAGES = {
    "Hà Nội": "hanoi.png",
    "Hồ Chí Minh": "hochiminh.png",
    "Đà Nẵng": "danang.png",
    "Thừa Thiên Huế": "hue.png",
    "Hải Phòng": "haiphong.png",
    "Cần Thơ": "cantho.png",
    # Thêm dần khi có ảnh mới
}

if st.session_state.selected_province:
    selected_data = gdf[gdf['NAME_1'] == st.session_state.selected_province]
    
    if selected_data.empty:
        st.warning(f"Không tìm thấy dữ liệu cho tỉnh: {st.session_state.selected_province}")
        st.session_state.selected_province = None
    else:
        row = selected_data.iloc[0]
        province = row['NAME_1']
        aqi_raw = row['AQI']
        update_date = row.get('Date', 'Không rõ')

        # Xử lý AQI (giữ nguyên logic cũ của bạn)
        if pd.isna(aqi_raw):
            aqi_display = "N/A"
            status = "Chưa có dữ liệu"
            status_color = "#999999"
        else:
            aqi = int(aqi_raw)
            aqi_display = str(aqi)
            if aqi <= 50:
                status, status_color = "Tốt", "#00e400"
            elif aqi <= 100:
                status, status_color = "Trung bình", "#cccc16"
            elif aqi <= 150:
                status, status_color = "Kém", "#ff7e00"
            elif aqi <= 200:
                status, status_color = "Xấu", "#ff0000"
            else:
                status, status_color = "Rất xấu", "#99004c"

        # LẤY ẢNH LOCAL
        filename = PROVINCE_IMAGES.get(province)
        img_path = IMG_DIR / filename if filename else None
        encoded = img_to_base64(img_path) if img_path else None
        bg_image = f"data:image/png;base64,{encoded}" if encoded else "https://i.imgur.com/2f8p8vP.jpg"  # fallback tạm

        # GIỮ NGUYÊN 100% STYLE CỦA BẠN – CHỈ ĐỔI URL ẢNH
        st.markdown(f"""
        <div class="bg-img" 
                 style="background: linear-gradient(to bottom, rgba(0,0,0,0.4), rgba(0,0,0,0.85)), 
                                    url('{bg_image}') center /cover no-repeat;">
            <div style="position: absolute; top: 20px; right: 30px; opacity: 0.8; font-size: 14px;">
                Cập nhật: {update_date}
            </div>
            <h1 style="margin:0; font-size: 58px; font-weight: bold; text-shadow: 0 6px 20px rgba(0,0,0,0.8);">
                {province}
            </h1>
            <h2 style="margin: -10px 0px 20px; font-size: 40px; font-weight: bold; color: {status_color}; 
                text-shadow: 0 6px 20px rgba(0,0,0,0.9);">
                {aqi_display} AQI - Tình Trạng : {status}
            </h2>
            <div style="font-size: 15px; font-weight: bold;">
                <span style="background: rgb(235 193 193 / 70%); 
                        padding: 12px 12px; border-radius: 80px; 
                        backdrop-filter: blur(15px); 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.6);">
                    Cuộn xuống để biết thêm chi tiết ▼
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    # Giữ nguyên phần chưa chọn tỉnh của bạn
    st.markdown("""
    <div style="
        margin-top: 24px;
        width: 100%;
        height: 340px;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
    ">
        Chọn một tỉnh từ bản đồ hoặc danh sách bên phải để xem chi tiết
    </div>
    """, unsafe_allow_html=True)

st.caption("**Dữ liệu cập nhật tự động lúc 8:00 AM** | Nguồn: AQICN + GADM")