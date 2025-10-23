import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os
import json
from io import BytesIO
import base64
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class AQIReportGenerator:
    """Lớp tạo báo cáo chất lượng không khí"""
    
    def __init__(self, db_path='data/processed/aqi_history.db'):
        self.db_path = db_path
        
    def load_data(self, start_date=None, end_date=None, province=None):
        """Tải dữ liệu AQI"""
        if not os.path.exists(self.db_path):
            return pd.DataFrame()
            
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Xây dựng query
            query = "SELECT * FROM daily_aqi WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND Date >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND Date <= ?"
                params.append(end_date)
                
            if province:
                query += " AND Province = ?"
                params.append(province)
            
            query += " ORDER BY Date"
            
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
                
            return df
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {e}")
            return pd.DataFrame()
    
    def generate_summary_report(self, start_date=None, end_date=None):
        """Tạo báo cáo tổng quan"""
        df = self.load_data(start_date, end_date)
        
        if df.empty:
            return {
                'error': 'Không có dữ liệu để tạo báo cáo',
                'summary': {},
                'charts': {}
            }
        
        # Thống kê cơ bản
        summary = {
            'total_records': len(df),
            'date_range': {
                'start': df['Date'].min().strftime('%Y-%m-%d'),
                'end': df['Date'].max().strftime('%Y-%m-%d')
            },
            'aqi_stats': {
                'mean': round(df['AQI'].mean(), 2),
                'median': round(df['AQI'].median(), 2),
                'std': round(df['AQI'].std(), 2),
                'min': round(df['AQI'].min(), 2),
                'max': round(df['AQI'].max(), 2)
            },
            'provinces_count': df['Province'].nunique(),
            'air_quality_distribution': self._get_air_quality_distribution(df)
        }
        
        # Tạo biểu đồ
        charts = self._create_summary_charts(df)
        
        return {
            'summary': summary,
            'charts': charts,
            'data': df
        }
    
    def generate_province_report(self, province, start_date=None, end_date=None):
        """Tạo báo cáo chi tiết cho một tỉnh"""
        df = self.load_data(start_date, end_date, province)
        
        if df.empty:
            return {
                'error': f'Không có dữ liệu cho tỉnh {province}',
                'summary': {},
                'charts': {}
            }
        
        # Thống kê cho tỉnh
        summary = {
            'province': province,
            'total_records': len(df),
            'date_range': {
                'start': df['Date'].min().strftime('%Y-%m-%d'),
                'end': df['Date'].max().strftime('%Y-%m-%d')
            },
            'aqi_stats': {
                'mean': round(df['AQI'].mean(), 2),
                'median': round(df['AQI'].median(), 2),
                'std': round(df['AQI'].std(), 2),
                'min': round(df['AQI'].min(), 2),
                'max': round(df['AQI'].max(), 2)
            },
            'trend': self._calculate_trend(df),
            'worst_days': self._get_worst_days(df, 5),
            'best_days': self._get_best_days(df, 5)
        }
        
        # Tạo biểu đồ
        charts = self._create_province_charts(df, province)
        
        return {
            'summary': summary,
            'charts': charts,
            'data': df
        }
    
    def generate_comparison_report(self, provinces, start_date=None, end_date=None):
        """Tạo báo cáo so sánh giữa các tỉnh"""
        all_data = []
        
        for province in provinces:
            df = self.load_data(start_date, end_date, province)
            if not df.empty:
                df['Province'] = province
                all_data.append(df)
        
        if not all_data:
            return {
                'error': 'Không có dữ liệu để so sánh',
                'summary': {},
                'charts': {}
            }
        
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Thống kê so sánh
        summary = {
            'provinces': provinces,
            'date_range': {
                'start': combined_df['Date'].min().strftime('%Y-%m-%d'),
                'end': combined_df['Date'].max().strftime('%Y-%m-%d')
            },
            'comparison_stats': self._get_comparison_stats(combined_df),
            'ranking': self._get_province_ranking(combined_df)
        }
        
        # Tạo biểu đồ so sánh
        charts = self._create_comparison_charts(combined_df)
        
        return {
            'summary': summary,
            'charts': charts,
            'data': combined_df
        }
    
    def _get_air_quality_distribution(self, df):
        """Phân bố chất lượng không khí"""
        def categorize_aqi(aqi):
            if pd.isna(aqi):
                return 'Không có dữ liệu'
            elif aqi <= 50:
                return 'Tốt'
            elif aqi <= 100:
                return 'Trung bình'
            elif aqi <= 150:
                return 'Không tốt cho nhóm nhạy cảm'
            elif aqi <= 200:
                return 'Không tốt'
            elif aqi <= 300:
                return 'Rất không tốt'
            else:
                return 'Nguy hiểm'
        
        df['Category'] = df['AQI'].apply(categorize_aqi)
        return df['Category'].value_counts().to_dict()
    
    def _calculate_trend(self, df):
        """Tính xu hướng AQI"""
        if len(df) < 2:
            return 'Không đủ dữ liệu'
        
        # Tính hệ số tương quan với thời gian
        df['time_numeric'] = (df['Date'] - df['Date'].min()).dt.days
        correlation = df['time_numeric'].corr(df['AQI'])
        
        if correlation > 0.1:
            return 'Tăng'
        elif correlation < -0.1:
            return 'Giảm'
        else:
            return 'Ổn định'
    
    def _get_worst_days(self, df, n=5):
        """Lấy n ngày có AQI cao nhất"""
        return df.nlargest(n, 'AQI')[['Date', 'AQI']].to_dict('records')
    
    def _get_best_days(self, df, n=5):
        """Lấy n ngày có AQI thấp nhất"""
        return df.nsmallest(n, 'AQI')[['Date', 'AQI']].to_dict('records')
    
    def _get_comparison_stats(self, df):
        """Thống kê so sánh giữa các tỉnh"""
        stats = df.groupby('Province')['AQI'].agg([
            'mean', 'median', 'std', 'min', 'max', 'count'
        ]).round(2)
        
        return stats.to_dict('index')
    
    def _get_province_ranking(self, df):
        """Xếp hạng các tỉnh theo chất lượng không khí"""
        ranking = df.groupby('Province')['AQI'].mean().sort_values().reset_index()
        ranking['Rank'] = range(1, len(ranking) + 1)
        return ranking.to_dict('records')
    
    def _create_summary_charts(self, df):
        """Tạo biểu đồ cho báo cáo tổng quan"""
        charts = {}
        
        # Biểu đồ xu hướng theo thời gian
        fig_trend = px.line(
            df, 
            x='Date', 
            y='AQI',
            color='Province',
            title='Xu hướng AQI theo thời gian'
        )
        charts['trend'] = fig_trend
        
        # Biểu đồ phân bố AQI
        fig_hist = px.histogram(
            df, 
            x='AQI',
            title='Phân bố AQI',
            nbins=20
        )
        charts['distribution'] = fig_hist
        
        # Biểu đồ tròn phân loại chất lượng
        df['Category'] = df['AQI'].apply(lambda x: self._get_aqi_category(x))
        category_counts = df['Category'].value_counts()
        
        fig_pie = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Phân bố chất lượng không khí'
        )
        charts['category_pie'] = fig_pie
        
        return charts
    
    def _create_province_charts(self, df, province):
        """Tạo biểu đồ cho báo cáo tỉnh"""
        charts = {}
        
        # Biểu đồ xu hướng
        fig_trend = px.line(
            df, 
            x='Date', 
            y='AQI',
            title=f'Xu hướng AQI - {province}'
        )
        charts['trend'] = fig_trend
        
        # Biểu đồ box plot
        fig_box = px.box(
            df, 
            y='AQI',
            title=f'Phân bố AQI - {province}'
        )
        charts['box_plot'] = fig_box
        
        # Biểu đồ heatmap theo tháng và ngày
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        
        pivot_data = df.pivot_table(
            values='AQI', 
            index='Day', 
            columns='Month', 
            aggfunc='mean'
        )
        
        fig_heatmap = px.imshow(
            pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            title=f'Heatmap AQI theo tháng - {province}',
            color_continuous_scale='RdYlGn_r'
        )
        charts['heatmap'] = fig_heatmap
        
        return charts
    
    def _create_comparison_charts(self, df):
        """Tạo biểu đồ so sánh"""
        charts = {}
        
        # Biểu đồ cột so sánh AQI trung bình
        avg_aqi = df.groupby('Province')['AQI'].mean().sort_values()
        
        fig_bar = px.bar(
            x=avg_aqi.values,
            y=avg_aqi.index,
            orientation='h',
            title='So sánh AQI trung bình giữa các tỉnh'
        )
        charts['avg_comparison'] = fig_bar
        
        # Biểu đồ box plot so sánh
        fig_box = px.box(
            df,
            x='Province',
            y='AQI',
            title='So sánh phân bố AQI giữa các tỉnh'
        )
        fig_box.update_xaxis(tickangle=45)
        charts['box_comparison'] = fig_box
        
        # Biểu đồ radar (nếu có đủ dữ liệu)
        if len(df['Province'].unique()) <= 6:  # Giới hạn số tỉnh cho biểu đồ radar
            radar_data = df.groupby('Province')['AQI'].agg(['mean', 'std', 'min', 'max']).reset_index()
            
            fig_radar = go.Figure()
            
            for _, row in radar_data.iterrows():
                fig_radar.add_trace(go.Scatterpolar(
                    r=[row['mean'], row['std'], row['min'], row['max']],
                    theta=['Trung bình', 'Độ lệch chuẩn', 'Tối thiểu', 'Tối đa'],
                    fill='toself',
                    name=row['Province']
                ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, max(radar_data['max'])]
                    )),
                title="So sánh radar AQI giữa các tỉnh"
            )
            charts['radar'] = fig_radar
        
        return charts
    
    def _get_aqi_category(self, aqi):
        """Phân loại AQI"""
        if pd.isna(aqi):
            return 'Không có dữ liệu'
        elif aqi <= 50:
            return 'Tốt'
        elif aqi <= 100:
            return 'Trung bình'
        elif aqi <= 150:
            return 'Không tốt cho nhóm nhạy cảm'
        elif aqi <= 200:
            return 'Không tốt'
        elif aqi <= 300:
            return 'Rất không tốt'
        else:
            return 'Nguy hiểm'
    
    def export_to_excel(self, report_data, filename=None):
        """Xuất báo cáo ra file Excel"""
        if filename is None:
            filename = f"aqi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet tổng quan
            if 'summary' in report_data:
                summary_df = pd.DataFrame([report_data['summary']])
                summary_df.to_excel(writer, sheet_name='Tổng quan', index=False)
            
            # Sheet dữ liệu
            if 'data' in report_data and not report_data['data'].empty:
                report_data['data'].to_excel(writer, sheet_name='Dữ liệu', index=False)
            
            # Sheet thống kê
            if 'summary' in report_data and 'aqi_stats' in report_data['summary']:
                stats_df = pd.DataFrame([report_data['summary']['aqi_stats']])
                stats_df.to_excel(writer, sheet_name='Thống kê', index=False)
        
        return filename
    
    def export_to_json(self, report_data, filename=None):
        """Xuất báo cáo ra file JSON"""
        if filename is None:
            filename = f"aqi_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Chuyển đổi datetime objects thành string
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            elif isinstance(obj, pd.Timestamp):
                return obj.isoformat()
            return obj
        
        # Xử lý dữ liệu trước khi xuất
        export_data = {}
        for key, value in report_data.items():
            if key == 'data' and isinstance(value, pd.DataFrame):
                export_data[key] = value.to_dict('records')
            else:
                export_data[key] = value
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=convert_datetime)
        
        return filename

def create_report_dashboard():
    """Tạo dashboard báo cáo cho Streamlit"""
    generator = AQIReportGenerator()
    
    # Báo cáo tổng quan
    summary_report = generator.generate_summary_report()
    
    return summary_report

if __name__ == "__main__":
    # Test tạo báo cáo
    generator = AQIReportGenerator()
    
    # Tạo báo cáo tổng quan
    report = generator.generate_summary_report()
    print("Báo cáo tổng quan:")
    print(json.dumps(report['summary'], indent=2, ensure_ascii=False))
    
    # Xuất ra file
    excel_file = generator.export_to_excel(report)
    print(f"Đã xuất báo cáo ra file: {excel_file}")
