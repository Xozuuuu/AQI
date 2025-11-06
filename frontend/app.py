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

with col2:
    # ===== SỬA LỖI TẠI ĐÂY =====
    
    # 1. HIỂN THỊ TITLE BAR (RIÊNG BIỆT)
    # Đây là phần sẽ ngang hàng với nút "Cập nhật"
    st.markdown('<div class="sidebar-title-box"><h3>Danh sách tỉnh</h3></div>', unsafe_allow_html=True)
    
    # 2. HIỂN THỊ DANH SÁCH CUỘN (SCROLLBAR)
    
    # Đọc và lọc dữ liệu
    gdf = gpd.read_file(config.DATA_PATH)
    gdf['AQI'] = pd.to_numeric(gdf['AQI'], errors='coerce')
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

st.caption("**Dữ liệu cập nhật tự động lúc 8:00 AM** | Nguồn: AQICN + GADM")