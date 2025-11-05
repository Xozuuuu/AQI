# frontend/app.py
import os
import sys

# THÊM ĐƯỜNG DẪN GỐC DỰ ÁN ĐỂ IMPORT backend & config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from streamlit_folium import st_folium  # THAY: st_folium thay vì folium_static
from frontend.visualize import create_map  # OK vì frontend là package

# =================================================================
# 1. CẤU HÌNH TRANG
# =================================================================
st.set_page_config(
    page_title="AirWatch VN",
    layout="wide"
)

# =================================================================
# 2. CSS ĐỂ BẢN ĐỒ TO HƠN (VÀ ẨN HEADER/FOOTER)
# =================================================================
st.markdown("""
<style>
.block-container {
    padding-top : 0.5rem;
    padding-bottom : 1rem;
    padding-left:5rem;
    padding-right:5rem;
}
/* === MỚI: Ẩn Header (chứa nút "Deploy") === */
[data-testid="stHeader"] {
    display: none;
}

/* === MỚI: Ẩn Footer (chứa "Made with Streamlit") === */
footer {
    display: none;
}
/* ============================================= */


/* Bắt iframe của st_folium */
iframe {
    width: 800px !important;      /* Rộng 70% theo code của bạn */
    height: 85vh !important;    /* Cao 85% màn hình */
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# =================================================================
# 3. NỘI DUNG CHÍNH
# =================================================================
st.title("AirWatch – Giám sát chất lượng không khí Việt Nam")
st.markdown("**Cập nhật AQI tự động từ AQICN, hiển thị theo tỉnh.**")

if st.button("Cập nhật dữ liệu AQI", type="primary"):
    with st.spinner("Đang lấy dữ liệu mới..."):
        try:
            from backend.data_processing import process_data
            process_data()
            st.success("Cập nhật thành công!")
        except Exception as e:
            st.error(f"Lỗi: {e}")

# =================================================================
# 4. BẢN ĐỒ
# =================================================================
with st.spinner("Đang vẽ bản đồ..."):
    m = create_map()
    st_folium(m, width=800, height=800, returned_objects=[])  # THAY: st_folium

# =================================================================
# 5. CHÚ THÍCH
# =================================================================
st.caption("Dữ liệu cập nhật tự động mỗi ngày lúc 8:00 AM. Nguồn: AQICN + GADM.")