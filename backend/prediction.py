import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class AQIPredictor:
    """Lớp dự báo AQI sử dụng machine learning"""
    
    def __init__(self, db_path='data/processed/aqi_history.db'):
        self.db_path = db_path
        self.models = {}
        self.poly_features = {}
        
    def load_historical_data(self, province=None):
        """Tải dữ liệu lịch sử AQI"""
        if not os.path.exists(self.db_path):
            return pd.DataFrame()
            
        try:
            conn = sqlite3.connect(self.db_path)
            if province:
                query = "SELECT * FROM daily_aqi WHERE Province = ? ORDER BY Date"
                df = pd.read_sql_query(query, conn, params=[province])
            else:
                query = "SELECT * FROM daily_aqi ORDER BY Date"
                df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date')
                df['day_of_year'] = df['Date'].dt.dayofyear
                df['month'] = df['Date'].dt.month
                df['day'] = df['Date'].dt.day
                
            return df
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu lịch sử: {e}")
            return pd.DataFrame()
    
    def prepare_features(self, df):
        """Chuẩn bị features cho model"""
        if df.empty:
            return np.array([]), np.array([])
            
        # Loại bỏ các giá trị AQI null
        df_clean = df.dropna(subset=['AQI'])
        
        if len(df_clean) < 3:
            return np.array([]), np.array([])
        
        # Features: ngày trong năm, tháng, ngày
        X = df_clean[['day_of_year', 'month', 'day']].values
        y = df_clean['AQI'].values
        
        return X, y
    
    def train_model(self, province):
        """Huấn luyện model cho một tỉnh"""
        df = self.load_historical_data(province)
        
        if df.empty or len(df) < 3:
            return False
            
        X, y = self.prepare_features(df)
        
        if len(X) < 3:
            return False
        
        try:
            # Sử dụng Polynomial Regression để bắt được xu hướng phi tuyến
            poly_features = PolynomialFeatures(degree=2)
            X_poly = poly_features.fit_transform(X)
            
            model = LinearRegression()
            model.fit(X_poly, y)
            
            # Lưu model và features
            self.models[province] = model
            self.poly_features[province] = poly_features
            
            return True
        except Exception as e:
            print(f"Lỗi khi huấn luyện model cho {province}: {e}")
            return False
    
    def predict_aqi(self, province, days_ahead=1):
        """Dự báo AQI cho một tỉnh"""
        if province not in self.models:
            if not self.train_model(province):
                return None
        
        try:
            # Tạo features cho ngày dự báo
            future_date = datetime.now() + timedelta(days=days_ahead)
            future_features = np.array([[
                future_date.timetuple().tm_yday,  # day_of_year
                future_date.month,                # month
                future_date.day                   # day
            ]])
            
            # Transform features
            poly_features = self.poly_features[province]
            future_features_poly = poly_features.transform(future_features)
            
            # Dự báo
            model = self.models[province]
            prediction = model.predict(future_features_poly)[0]
            
            # Đảm bảo AQI không âm
            prediction = max(0, prediction)
            
            return round(prediction, 1)
        except Exception as e:
            print(f"Lỗi khi dự báo AQI cho {province}: {e}")
            return None
    
    def predict_all_provinces(self, days_ahead=1):
        """Dự báo AQI cho tất cả các tỉnh"""
        # Lấy danh sách tỉnh từ dữ liệu lịch sử
        df = self.load_historical_data()
        provinces = df['Province'].unique() if not df.empty else []
        
        predictions = []
        for province in provinces:
            aqi_pred = self.predict_aqi(province, days_ahead)
            if aqi_pred is not None:
                predictions.append({
                    'Province': province,
                    'Predicted_AQI': aqi_pred,
                    'Prediction_Date': datetime.now() + timedelta(days=days_ahead),
                    'Days_Ahead': days_ahead
                })
        
        return pd.DataFrame(predictions)
    
    def get_air_quality_alerts(self, threshold_aqi=150):
        """Tạo cảnh báo chất lượng không khí"""
        predictions = self.predict_all_provinces()
        alerts = []
        
        for _, row in predictions.iterrows():
            aqi = row['Predicted_AQI']
            province = row['Province']
            
            if aqi >= threshold_aqi:
                alert_level = self._get_alert_level(aqi)
                alerts.append({
                    'Province': province,
                    'AQI': aqi,
                    'Alert_Level': alert_level,
                    'Message': self._get_alert_message(province, aqi, alert_level),
                    'Date': row['Prediction_Date']
                })
        
        return pd.DataFrame(alerts)
    
    def _get_alert_level(self, aqi):
        """Xác định mức độ cảnh báo"""
        if aqi <= 50:
            return "Tốt"
        elif aqi <= 100:
            return "Trung bình"
        elif aqi <= 150:
            return "Không tốt cho nhóm nhạy cảm"
        elif aqi <= 200:
            return "Không tốt"
        elif aqi <= 300:
            return "Rất không tốt"
        else:
            return "Nguy hiểm"
    
    def _get_alert_message(self, province, aqi, alert_level):
        """Tạo thông báo cảnh báo"""
        if alert_level in ["Không tốt", "Rất không tốt", "Nguy hiểm"]:
            return f"⚠️ CẢNH BÁO: Chất lượng không khí tại {province} dự kiến ở mức {alert_level} (AQI: {aqi}). Khuyến nghị hạn chế hoạt động ngoài trời."
        elif alert_level == "Không tốt cho nhóm nhạy cảm":
            return f"🔶 LƯU Ý: Nhóm nhạy cảm nên cẩn thận tại {province} (AQI: {aqi})."
        else:
            return f"✅ Chất lượng không khí tại {province} dự kiến tốt (AQI: {aqi})."

class WeatherBasedPredictor:
    """Lớp dự báo AQI dựa trên dữ liệu thời tiết (mô phỏng)"""
    
    def __init__(self):
        self.weather_factors = {
            'temperature': 0.3,    # Nhiệt độ cao -> AQI cao hơn
            'humidity': -0.2,      # Độ ẩm cao -> AQI thấp hơn
            'wind_speed': -0.4,    # Gió mạnh -> AQI thấp hơn
            'pressure': 0.1        # Áp suất cao -> AQI cao hơn
        }
    
    def get_weather_data(self, province):
        """Lấy dữ liệu thời tiết (mô phỏng)"""
        # Trong thực tế, sẽ kết nối với API thời tiết
        # Ở đây tôi sẽ tạo dữ liệu mô phỏng
        np.random.seed(hash(province) % 2**32)
        
        return {
            'temperature': np.random.normal(28, 5),  # Nhiệt độ trung bình 28°C
            'humidity': np.random.normal(70, 15),    # Độ ẩm trung bình 70%
            'wind_speed': np.random.exponential(3),  # Tốc độ gió
            'pressure': np.random.normal(1013, 10)   # Áp suất khí quyển
        }
    
    def predict_aqi_with_weather(self, base_aqi, province):
        """Dự báo AQI dựa trên thời tiết"""
        weather = self.get_weather_data(province)
        
        # Tính toán ảnh hưởng của thời tiết
        weather_impact = 0
        for factor, weight in self.weather_factors.items():
            weather_impact += weather[factor] * weight
        
        # Điều chỉnh AQI dựa trên thời tiết
        adjusted_aqi = base_aqi * (1 + weather_impact / 100)
        
        return max(0, round(adjusted_aqi, 1))

def create_prediction_dashboard():
    """Tạo dashboard dự báo cho Streamlit"""
    predictor = AQIPredictor()
    weather_predictor = WeatherBasedPredictor()
    
    # Dự báo cho tất cả tỉnh
    predictions = predictor.predict_all_provinces()
    
    if predictions.empty:
        return "Không có dữ liệu để dự báo."
    
    # Thêm dự báo dựa trên thời tiết
    predictions['Weather_Adjusted_AQI'] = predictions.apply(
        lambda row: weather_predictor.predict_aqi_with_weather(
            row['Predicted_AQI'], row['Province']
        ), axis=1
    )
    
    return predictions

if __name__ == "__main__":
    # Test dự báo
    predictor = AQIPredictor()
    predictions = predictor.predict_all_provinces()
    print("Dự báo AQI:")
    print(predictions)
    
    # Test cảnh báo
    alerts = predictor.get_air_quality_alerts()
    print("\nCảnh báo chất lượng không khí:")
    print(alerts)
