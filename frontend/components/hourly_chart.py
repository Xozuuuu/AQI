# frontend/components/hourly_chart.py
import plotly.graph_objects as go
from backend.hourly_forecast import get_hourly_forecast

def create_hourly_chart(province_name):
    if not province_name:
        return None
        
    data = get_hourly_forecast(province_name)
    
    times = [item["display_label"] for item in data]
    aqi_values = [item["aqi"] for item in data]
    colors = [item["color"] for item in data]
    statuses = [item["status"] for item in data]
    
    fig = go.Figure()
    
    # Đường cong chính
    fig.add_trace(go.Scatter(
        x=times,
        y=aqi_values,
        mode='lines+markers',
        line=dict(color='#6366f1', width=5, shape='spline', smoothing=1.3),
        marker=dict(
            size=16,
            color=colors,
            line=dict(width=3, color='white')
        ),
        hovertemplate='<b>%{x}</b><br>AQI: <b>%{y}</b><br>%{text}<extra></extra>',
        text=statuses,
        name=""
    ))

    # SỬA ĐIỂM ĐẦU TIÊN: to hơn + viền đen
    with fig.batch_update():
        new_sizes = [20 if i == 0 else 16 for i in range(len(aqi_values))]
        new_line_widths = [5 if i == 0 else 3 for i in range(len(aqi_values))]
        new_line_colors = ['black' if i == 0 else 'white' for i in range(len(aqi_values))]
        
        fig.data[0].marker.size = new_sizes
        fig.data[0].marker.line.width = new_line_widths
        fig.data[0].marker.line.color = new_line_colors

    fig.update_layout(
        title={
            'text': f"Dự báo 24 giờ của tỉnh: <b>{province_name}</b>",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=24, color="white")
        },
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(15,23,42,0.95)",
        height=350,
        margin=dict(l=50, r=50, t=80, b=100),
        xaxis=dict(
            tickfont=dict(size=14, color="white"),
            gridcolor="rgba(255,255,255,0.15)",
            zeroline=False
        ),
        yaxis=dict(
            range=[0, max(max(aqi_values), 100) * 1.3],
            showgrid=True,
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="white"),
            title=dict(
                text="AQI",
                font=dict(color="white",size=16)
            )
        ),
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),
        showlegend=False
    )

    # Icon + trạng thái dưới mỗi điểm
    icon_map = {"Tốt": "Smiling Face", "Trung bình": "Neutral Face", "Kém": "Face with Mask", "Xấu": "Dizzy Face", "Rất xấu": "Face Vomiting", "Nguy hại": "Skull"}
    for i, item in enumerate(data):
        fig.add_annotation(
            x=times[i],
            y=-15,
            text=icon_map.get(item["status"], "Neutral Face"),
            showarrow=False,
            font=dict(size=36),
            yshift=10
        )
        fig.add_annotation(
            x=times[i],
            y=-40,
            text=item["status"],
            showarrow=False,
            font=dict(size=12, color="white"),
            bgcolor=item["color"],
            bordercolor="white",
            borderwidth=2,
            borderpad=6,
            opacity=0.9
        )
    
    return fig