# frontend/app.py
import os
import sys

# THÊM ĐƯỜNG DẪN GỐC DỰ ÁN ĐỂ IMPORT backend & config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from streamlit_folium import folium_static
from frontend.visualize import create_map  # OK vì frontend là package

st.set_page_config(page_title="AirWatch VN", layout="wide")

st.title("AirWatch – Giám sát chất lượng không khí Việt Nam")
st.markdown("**Cập nhật AQI tự động từ AQICN, hiển thị theo tỉnh.**")

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("Cập nhật dữ liệu AQI", type="primary"):
        with st.spinner("Đang lấy dữ liệu mới..."):
            try:
                from backend.data_processing import process_data  # BÂY GIỜ OK!
                process_data()
                st.success("Cập nhật thành công!")
            except Exception as e:
                st.error(f"Lỗi: {e}")

with col2:
    st.empty()

# Tạo và hiển thị bản đồ
with st.spinner("Đang vẽ bản đồ..."):
    m = create_map()
    folium_static(m, width=1200, height=600)

st.caption("Dữ liệu cập nhật tự động mỗi ngày lúc 8:00 AM. Nguồn: AQICN + GADM.")