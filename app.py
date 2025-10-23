import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import sqlite3
import os
import sys

# Thêm đường dẫn để import các module nội bộ
sys.path.append(os.path.dirname(__file__))

from backend.fetch_aqi import fetch_aqi
from backend.data_processing import process_data
from backend.prediction import AQIPredictor, WeatherBasedPredictor, create_prediction_dashboard
from backend.reporting import AQIReportGenerator, create_report_dashboard
import config

# Cấu hình trang
st.set_page_config(
    page_title="Hệ thống Giám sát Chất lượng Không khí Thông minh",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .aqi-good { background-color: #00e400; color: white; }
    .aqi-moderate { background-color: #ffff00; color: black; }
    .aqi-unhealthy-sensitive { background-color: #ff7e00; color: white; }
    .aqi-unhealthy { background-color: #ff0000; color: white; }
    .aqi-very-unhealthy { background-color: #8f3f97; color: white; }
    .aqi-hazardous { background-color: #7e0023; color: white; }
</style>
""", unsafe_allow_html=True)

def get_aqi_category(aqi):
    """Phân loại AQI theo tiêu chuẩn"""
    if pd.isna(aqi) or aqi is None:
        return "Không có dữ liệu", "aqi-unknown"
    
    aqi = float(aqi)
    if aqi <= 50:
        return "Tốt", "aqi-good"
    elif aqi <= 100:
        return "Trung bình", "aqi-moderate"
    elif aqi <= 150:
        return "Không tốt cho nhóm nhạy cảm", "aqi-unhealthy-sensitive"
    elif aqi <= 200:
        return "Không tốt", "aqi-unhealthy"
    elif aqi <= 300:
        return "Rất không tốt", "aqi-very-unhealthy"
    else:
        return "Nguy hiểm", "aqi-hazardous"

def load_data():
    """Tải dữ liệu AQI"""
    try:
        # Thử tải dữ liệu mới nhất
        df = fetch_aqi()
        return df
    except Exception as e:
        st.error(f"Lỗi khi tải dữ liệu: {e}")
        # Fallback: tải dữ liệu từ file
        if os.path.exists('data/raw/latest_aqi.csv'):
            return pd.read_csv('data/raw/latest_aqi.csv')
        return pd.DataFrame()

def create_map(df):
    """Tạo bản đồ tương tác với Folium"""
    # Tọa độ trung tâm Việt Nam
    center_lat, center_lon = 16.0, 108.0
    
    # Tạo bản đồ
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles='OpenStreetMap'
    )
    
    # Thêm các điểm AQI
    for idx, row in df.iterrows():
        if pd.notna(row['AQI']):
            # Tọa độ giả lập cho các tỉnh (có thể cải thiện bằng shapefile)
            coords = get_province_coords(row['Province'])
            if coords:
                lat, lon = coords
                
                # Màu sắc theo AQI
                category, css_class = get_aqi_category(row['AQI'])
                color = get_aqi_color(row['AQI'])
                
                # Tạo popup
                popup_text = f"""
                <b>{row['Province']}</b><br>
                AQI: {row['AQI']}<br>
                Mức độ: {category}<br>
                Thời gian: {row['Date']}
                """
                
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=15,
                    popup=folium.Popup(popup_text, max_width=200),
                    color='black',
                    weight=2,
                    fillColor=color,
                    fillOpacity=0.7
                ).add_to(m)
    
    return m

def get_province_coords(province):
    """Lấy tọa độ của tỉnh (giả lập)"""
    coords_map = {
        'Ha Noi': (21.0285, 105.8542),
        'Ho Chi Minh City': (10.8231, 106.6297),
        'Da Nang': (16.0544, 108.2022),
        'Can Tho': (10.0452, 105.7469),
        'Hai Phong': (20.8449, 106.6881),
        'Thai Nguyen': (21.5944, 105.8481),
        'Bac Ninh': (21.1861, 106.0763),
        'Hung Yen': (20.6466, 106.0516),
        'Quang Ninh': (21.0064, 107.2926),
        'Thai Binh': (20.4465, 106.3421),
        'Ha Nam': (20.5431, 105.9229),
        'Ninh Binh': (20.2506, 105.9744),
        'Quang Binh': (17.4683, 106.6226),
        'Thua Thien Hue': (16.4637, 107.5909),
        'Gia Lai': (13.9838, 108.0000),
        'Nha Trang': (12.2388, 109.1967),
        'Lam Dong': (11.9404, 108.4583),
        'Tay Ninh': (11.3144, 106.1093),
        'Vung Tau': (10.3459, 107.0843),
        'Vinh Long': (10.2536, 105.9756),
        'Tra Vinh': (9.9349, 106.3450),
        'Bac Giang': (21.2739, 106.1946),
        'Viet Tri': (21.3008, 105.4306)
    }
    return coords_map.get(province)

def get_aqi_color(aqi):
    """Lấy màu sắc theo AQI"""
    if pd.isna(aqi) or aqi is None:
        return '#808080'
    
    aqi = float(aqi)
    if aqi <= 50:
        return '#00e400'
    elif aqi <= 100:
        return '#ffff00'
    elif aqi <= 150:
        return '#ff7e00'
    elif aqi <= 200:
        return '#ff0000'
    elif aqi <= 300:
        return '#8f3f97'
    else:
        return '#7e0023'

def main():
    # Header chính
    st.markdown('<h1 class="main-header">🌍 Hệ thống Giám sát Chất lượng Không khí Thông minh</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Điều khiển")
    
    # Menu điều hướng
    page = st.sidebar.selectbox(
        "Chọn trang",
        ["📊 Dashboard", "🔮 Dự báo", "📈 Báo cáo", "⚙️ Cài đặt"]
    )
    
    # Nút cập nhật dữ liệu
    if st.sidebar.button("🔄 Cập nhật dữ liệu", type="primary"):
        with st.spinner("Đang cập nhật dữ liệu..."):
            df = fetch_aqi()
            os.makedirs('data/raw', exist_ok=True)
            df.to_csv('data/raw/latest_aqi.csv', index=False, encoding='utf-8-sig')
            
            # Lưu vào database lịch sử
            try:
                process_data()
                st.success("Cập nhật thành công!")
            except Exception as e:
                st.warning(f"Cập nhật dữ liệu thành công nhưng có lỗi khi lưu lịch sử: {e}")
            st.rerun()
    
    # Điều hướng trang
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "🔮 Dự báo":
        show_prediction_page()
    elif page == "📈 Báo cáo":
        show_reporting_page()
    elif page == "⚙️ Cài đặt":
        show_settings_page()

def show_dashboard():
    # Tải dữ liệu
    df = load_data()
    
    if df.empty:
        st.error("Không có dữ liệu để hiển thị. Vui lòng cập nhật dữ liệu.")
        return
    
    # Thống kê tổng quan
    st.subheader("📊 Thống kê tổng quan")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_provinces = len(df)
        st.metric("Tổng số tỉnh", total_provinces)
    
    with col2:
        avg_aqi = df['AQI'].mean()
        st.metric("AQI trung bình", f"{avg_aqi:.1f}" if not pd.isna(avg_aqi) else "N/A")
    
    with col3:
        max_aqi = df['AQI'].max()
        st.metric("AQI cao nhất", f"{max_aqi:.1f}" if not pd.isna(max_aqi) else "N/A")
    
    with col4:
        min_aqi = df['AQI'].min()
        st.metric("AQI thấp nhất", f"{min_aqi:.1f}" if not pd.isna(min_aqi) else "N/A")
    
    # Bảng dữ liệu chi tiết
    st.subheader("📋 Dữ liệu chi tiết")
    
    # Tạo bảng với định dạng màu sắc
    df_display = df.copy()
    df_display['Mức độ'] = df_display['AQI'].apply(lambda x: get_aqi_category(x)[0])
    
    st.dataframe(
        df_display[['Province', 'AQI', 'Mức độ', 'Date']],
        use_container_width=True,
        hide_index=True
    )
    
    # Biểu đồ phân bố AQI
    st.subheader("📈 Biểu đồ phân bố AQI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Biểu đồ cột
        fig_bar = px.bar(
            df, 
            x='Province', 
            y='AQI',
            title="AQI theo tỉnh",
            color='AQI',
            color_continuous_scale='RdYlGn_r'
        )
        fig_bar.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Biểu đồ tròn phân loại AQI
        df['Category'] = df['AQI'].apply(lambda x: get_aqi_category(x)[0])
        category_counts = df['Category'].value_counts()
        
        fig_pie = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Phân bố mức độ chất lượng không khí"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Bản đồ tương tác
    st.subheader("🗺️ Bản đồ tương tác")
    
    if not df.empty:
        map_obj = create_map(df)
        st_folium(map_obj, width=700, height=500)
    
    # Phân tích xu hướng (nếu có dữ liệu lịch sử)
    st.subheader("📈 Phân tích xu hướng")
    
    if os.path.exists('data/processed/aqi_history.db'):
        try:
            conn = sqlite3.connect('data/processed/aqi_history.db')
            history_df = pd.read_sql_query("SELECT * FROM daily_aqi ORDER BY Date", conn)
            conn.close()
            
            if not history_df.empty:
                # Chuyển đổi cột Date
                history_df['Date'] = pd.to_datetime(history_df['Date'])
                
                # Biểu đồ xu hướng
                fig_trend = px.line(
                    history_df, 
                    x='Date', 
                    y='AQI',
                    color='Province',
                    title="Xu hướng AQI theo thời gian"
                )
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("Chưa có dữ liệu lịch sử để phân tích xu hướng.")
        except Exception as e:
            st.warning(f"Không thể tải dữ liệu lịch sử: {e}")
    else:
        st.info("Chưa có dữ liệu lịch sử để phân tích xu hướng.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🌍 Hệ thống Giám sát Chất lượng Không khí Thông minh | 
        Được phát triển với Python, Streamlit, Folium, GeoPandas</p>
    </div>
    """, unsafe_allow_html=True)

def show_prediction_page():
    """Trang dự báo chất lượng không khí"""
    st.header("🔮 Dự báo Chất lượng Không khí")
    
    # Khởi tạo predictor
    predictor = AQIPredictor()
    weather_predictor = WeatherBasedPredictor()
    
    # Cài đặt dự báo
    col1, col2 = st.columns(2)
    
    with col1:
        days_ahead = st.slider("Số ngày dự báo", 1, 7, 1)
    
    with col2:
        threshold = st.slider("Ngưỡng cảnh báo AQI", 50, 300, 150)
    
    # Nút dự báo
    if st.button("🔮 Thực hiện dự báo", type="primary"):
        with st.spinner("Đang thực hiện dự báo..."):
            # Dự báo cho tất cả tỉnh
            predictions = predictor.predict_all_provinces(days_ahead)
            
            if not predictions.empty:
                # Thêm dự báo dựa trên thời tiết
                predictions['Weather_Adjusted_AQI'] = predictions.apply(
                    lambda row: weather_predictor.predict_aqi_with_weather(
                        row['Predicted_AQI'], row['Province']
                    ), axis=1
                )
                
                # Hiển thị kết quả dự báo
                st.subheader("📊 Kết quả dự báo")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.dataframe(
                        predictions[['Province', 'Predicted_AQI', 'Weather_Adjusted_AQI', 'Prediction_Date']],
                        use_container_width=True
                    )
                
                with col2:
                    # Biểu đồ so sánh dự báo
                    fig = px.bar(
                        predictions,
                        x='Province',
                        y=['Predicted_AQI', 'Weather_Adjusted_AQI'],
                        title=f'Dự báo AQI cho {days_ahead} ngày tới',
                        barmode='group'
                    )
                    fig.update_xaxis(tickangle=45)
                    st.plotly_chart(fig, use_container_width=True)
                
                # Cảnh báo chất lượng không khí
                alerts = predictor.get_air_quality_alerts(threshold)
                
                if not alerts.empty:
                    st.subheader("⚠️ Cảnh báo chất lượng không khí")
                    
                    for _, alert in alerts.iterrows():
                        st.warning(f"**{alert['Province']}**: {alert['Message']}")
                else:
                    st.success("✅ Không có cảnh báo chất lượng không khí nào.")
            else:
                st.error("Không thể thực hiện dự báo. Vui lòng kiểm tra dữ liệu lịch sử.")

def show_reporting_page():
    """Trang báo cáo và phân tích"""
    st.header("📈 Báo cáo và Phân tích")
    
    # Khởi tạo report generator
    generator = AQIReportGenerator()
    
    # Cài đặt báo cáo
    col1, col2 = st.columns(2)
    
    with col1:
        report_type = st.selectbox(
            "Loại báo cáo",
            ["Tổng quan", "Theo tỉnh", "So sánh tỉnh"]
        )
    
    with col2:
        if report_type == "Theo tỉnh":
            # Lấy danh sách tỉnh
            df = load_data()
            provinces = df['Province'].unique().tolist() if not df.empty else []
            selected_province = st.selectbox("Chọn tỉnh", provinces)
        elif report_type == "So sánh tỉnh":
            df = load_data()
            provinces = df['Province'].unique().tolist() if not df.empty else []
            selected_provinces = st.multiselect("Chọn các tỉnh", provinces, default=provinces[:3])
    
    # Nút tạo báo cáo
    if st.button("📊 Tạo báo cáo", type="primary"):
        with st.spinner("Đang tạo báo cáo..."):
            if report_type == "Tổng quan":
                report = generator.generate_summary_report()
            elif report_type == "Theo tỉnh":
                report = generator.generate_province_report(selected_province)
            elif report_type == "So sánh tỉnh":
                report = generator.generate_comparison_report(selected_provinces)
            
            if 'error' in report:
                st.error(report['error'])
            else:
                # Hiển thị tóm tắt
                st.subheader("📋 Tóm tắt báo cáo")
                
                if 'summary' in report:
                    summary = report['summary']
                    
                    # Thống kê cơ bản
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if 'total_records' in summary:
                            st.metric("Tổng số bản ghi", summary['total_records'])
                        if 'provinces_count' in summary:
                            st.metric("Số tỉnh", summary['provinces_count'])
                    
                    with col2:
                        if 'aqi_stats' in summary:
                            aqi_stats = summary['aqi_stats']
                            st.metric("AQI trung bình", f"{aqi_stats.get('mean', 'N/A')}")
                            st.metric("AQI cao nhất", f"{aqi_stats.get('max', 'N/A')}")
                    
                    with col3:
                        if 'aqi_stats' in summary:
                            aqi_stats = summary['aqi_stats']
                            st.metric("AQI thấp nhất", f"{aqi_stats.get('min', 'N/A')}")
                            st.metric("Độ lệch chuẩn", f"{aqi_stats.get('std', 'N/A')}")
                
                # Hiển thị biểu đồ
                if 'charts' in report:
                    st.subheader("📊 Biểu đồ phân tích")
                    
                    for chart_name, chart in report['charts'].items():
                        st.plotly_chart(chart, use_container_width=True)
                
                # Nút xuất báo cáo
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📥 Xuất Excel"):
                        filename = generator.export_to_excel(report)
                        st.success(f"Đã xuất báo cáo ra file: {filename}")
                
                with col2:
                    if st.button("📥 Xuất JSON"):
                        filename = generator.export_to_json(report)
                        st.success(f"Đã xuất báo cáo ra file: {filename}")

def show_settings_page():
    """Trang cài đặt"""
    st.header("⚙️ Cài đặt Hệ thống")
    
    # Cài đặt API
    st.subheader("🔑 Cài đặt API")
    
    with st.expander("Cấu hình API AQI"):
        st.info("API Key hiện tại được cấu hình trong file config.py")
        st.code(f"API_KEY = {config.API_KEY[:10]}...")
    
    # Cài đặt dữ liệu
    st.subheader("💾 Quản lý Dữ liệu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Xóa dữ liệu lịch sử"):
            if os.path.exists('data/processed/aqi_history.db'):
                os.remove('data/processed/aqi_history.db')
                st.success("Đã xóa dữ liệu lịch sử!")
            else:
                st.info("Không có dữ liệu lịch sử để xóa.")
    
    with col2:
        if st.button("📊 Tạo dữ liệu mẫu"):
            # Tạo dữ liệu mẫu
            sample_data = []
            provinces = list(config.PROVINCE_MAPPING.values())
            
            for i in range(30):  # 30 ngày dữ liệu mẫu
                date = datetime.now() - timedelta(days=i)
                for province in provinces:
                    sample_data.append({
                        'Province': province,
                        'AQI': np.random.randint(20, 200),
                        'Date': date
                    })
            
            df_sample = pd.DataFrame(sample_data)
            
            # Lưu vào database
            os.makedirs('data/processed', exist_ok=True)
            conn = sqlite3.connect('data/processed/aqi_history.db')
            df_sample.to_sql('daily_aqi', conn, if_exists='replace', index=False)
            conn.close()
            
            st.success("Đã tạo dữ liệu mẫu!")
    
    # Thông tin hệ thống
    st.subheader("ℹ️ Thông tin Hệ thống")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.metric("Số tỉnh được giám sát", len(config.PROVINCES_LIST))
        st.metric("Dung lượng dữ liệu", f"{os.path.getsize('data/raw/latest_aqi.csv') / 1024:.1f} KB" if os.path.exists('data/raw/latest_aqi.csv') else "0 KB")
    
    with info_col2:
        st.metric("Phiên bản Python", f"{sys.version.split()[0]}")
        st.metric("Trạng thái", "🟢 Hoạt động")

if __name__ == "__main__":
    main()
