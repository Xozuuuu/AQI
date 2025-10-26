# frontend/visualize.py
import folium
import geopandas as gpd
import config
import pandas as pd

def create_map():
    # Đọc GeoJSON
    gdf = gpd.read_file(config.DATA_PATH)
    
    # Bản đồ
    m = folium.Map(location=[16.0, 107.0], zoom_start=6, tiles='CartoDB positron')
    
    # Màu theo AQI
    def get_color(aqi):
        if pd.isna(aqi): return '#ffffff'  # TRẮNG nếu không có AQI
        aqi = float(aqi)
        if aqi <= 50:  return '#00e400'
        if aqi <= 100: return '#ffff00'
        if aqi <= 150: return '#ff7e00'
        if aqi <= 200: return '#ff0000'
        if aqi <= 300: return '#99004c'
        return '#4d0000'
    
    # Thêm từng tỉnh
    for _, row in gdf.iterrows():
        aqi = row['AQI']
        geojson = row['geometry'].__geo_interface__
        
        popup = f"""
        <b>{row['NAME_1']}</b><br>
        AQI: <b>{aqi if not pd.isna(aqi) else 'Chưa có dữ liệu'}</b><br>
        Cập nhật: {row['Date']}
        """
        
        folium.GeoJson(
            geojson,
            style_function=lambda x, aqi=aqi: {
                'fillColor': get_color(aqi),
                'color': '#666666',
                'weight': 1.2,
                'fillOpacity': 0.7 if not pd.isna(aqi) else 0.3,
            },
            popup=folium.Popup(popup, max_width=300)
        ).add_to(m)
    
    # Legend
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; 
                background: white; padding: 12px; border: 2px solid #333; border-radius: 8px; font-family: Arial;">
        <p style="margin:0; font-weight:bold; font-size:14px;">AQI (Demo)</p>
        <p style="margin:3px 0;"><i style="background:#00e400; width:18px; height:18px; display:inline-block;"></i> 0-50: Tốt</p>
        <p style="margin:3px 0;"><i style="background:#ffff00; width:18px; height:18px; display:inline-block;"></i> 51-100: Trung bình</p>
        <p style="margin:3px 0;"><i style="background:#ff7e00; width:18px; height:18px; display:inline-block;"></i> 101-150: Kém</p>
        <p style="margin:3px 0;"><i style="background:#ff0000; width:18px; height:18px; display:inline-block;"></i> 151-200: Xấu</p>
        <p style="margin:3px 0; color:#999;"><i style="background:#ffffff; width:18px; height:18px; display:inline-block; border:1px solid #ccc;"></i> Chưa có dữ liệu</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m