import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import List, Dict, Optional, Tuple

class AQIDatabase:
    """Lớp quản lý database SQLite cho hệ thống AQI"""
    
    def __init__(self, db_path: str = 'data/processed/aqi_monitoring.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Khởi tạo database và tạo các bảng cần thiết"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Bảng lưu dữ liệu AQI hàng ngày
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_aqi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    province TEXT NOT NULL,
                    aqi INTEGER,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(province, date)
                )
            ''')
            
            # Bảng lưu dữ liệu AQI theo giờ (nếu cần)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hourly_aqi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    province TEXT NOT NULL,
                    aqi INTEGER,
                    datetime TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(province, datetime)
                )
            ''')
            
            # Bảng lưu lịch sử thay đổi AQI
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS aqi_changes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    province TEXT NOT NULL,
                    old_aqi INTEGER,
                    new_aqi INTEGER,
                    change_amount INTEGER,
                    change_percentage REAL,
                    date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bảng lưu thống kê AQI
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS aqi_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    province TEXT NOT NULL,
                    date DATE NOT NULL,
                    min_aqi INTEGER,
                    max_aqi INTEGER,
                    avg_aqi REAL,
                    median_aqi REAL,
                    std_aqi REAL,
                    total_records INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(province, date)
                )
            ''')
            
            # Tạo indexes để tối ưu performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_daily_aqi_province ON daily_aqi(province)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_daily_aqi_date ON daily_aqi(date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_daily_aqi_province_date ON daily_aqi(province, date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_hourly_aqi_province ON hourly_aqi(province)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_hourly_aqi_datetime ON hourly_aqi(datetime)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_aqi_changes_province ON aqi_changes(province)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_aqi_changes_date ON aqi_changes(date)')
            
            conn.commit()
    
    def save_daily_aqi(self, aqi_data: pd.DataFrame) -> bool:
        """Lưu dữ liệu AQI hàng ngày"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Lưu dữ liệu mới
                aqi_data.to_sql('daily_aqi', conn, if_exists='append', index=False)
                
                # Cập nhật thống kê
                self._update_statistics(aqi_data)
                
                # Kiểm tra thay đổi và lưu vào bảng changes
                self._track_changes(aqi_data)
                
                return True
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu AQI: {e}")
            return False
    
    def get_latest_aqi(self, province: Optional[str] = None) -> pd.DataFrame:
        """Lấy dữ liệu AQI mới nhất"""
        with sqlite3.connect(self.db_path) as conn:
            if province:
                query = '''
                    SELECT * FROM daily_aqi 
                    WHERE province = ? 
                    ORDER BY date DESC 
                    LIMIT 1
                '''
                return pd.read_sql_query(query, conn, params=[province])
            else:
                query = '''
                    SELECT province, aqi, date, created_at
                    FROM daily_aqi d1
                    WHERE d1.date = (
                        SELECT MAX(d2.date) 
                        FROM daily_aqi d2 
                        WHERE d2.province = d1.province
                    )
                    ORDER BY province
                '''
                return pd.read_sql_query(query, conn)
    
    def get_historical_aqi(self, province: str, days: int = 30) -> pd.DataFrame:
        """Lấy dữ liệu AQI lịch sử"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT * FROM daily_aqi 
                WHERE province = ? 
                AND date >= date('now', '-{} days')
                ORDER BY date DESC
            '''.format(days)
            return pd.read_sql_query(query, conn, params=[province])
    
    def compare_aqi_data(self, new_data: pd.DataFrame) -> Dict:
        """So sánh dữ liệu mới với dữ liệu cũ"""
        comparison_result = {
            'new_records': [],
            'updated_records': [],
            'no_change_records': [],
            'summary': {}
        }
        
        try:
            # Lấy dữ liệu cũ nhất (hôm qua)
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            with sqlite3.connect(self.db_path) as conn:
                for _, new_row in new_data.iterrows():
                    province = new_row['Province']
                    new_aqi = new_row['AQI']
                    
                    # Lấy dữ liệu cũ
                    old_query = '''
                        SELECT aqi FROM daily_aqi 
                        WHERE province = ? AND date = ?
                    '''
                    old_result = pd.read_sql_query(old_query, conn, params=[province, yesterday])
                    
                    if old_result.empty:
                        # Dữ liệu mới hoàn toàn
                        comparison_result['new_records'].append({
                            'province': province,
                            'new_aqi': new_aqi,
                            'old_aqi': None,
                            'change': None,
                            'change_percentage': None
                        })
                    else:
                        old_aqi = old_result['aqi'].iloc[0]
                        change = new_aqi - old_aqi if pd.notna(new_aqi) and pd.notna(old_aqi) else None
                        change_percentage = (change / old_aqi * 100) if change is not None and old_aqi != 0 else None
                        
                        record = {
                            'province': province,
                            'new_aqi': new_aqi,
                            'old_aqi': old_aqi,
                            'change': change,
                            'change_percentage': change_percentage
                        }
                        
                        if change is None:
                            comparison_result['no_change_records'].append(record)
                        elif abs(change) < 5:  # Thay đổi nhỏ
                            comparison_result['no_change_records'].append(record)
                        else:
                            comparison_result['updated_records'].append(record)
            
            # Tạo summary
            comparison_result['summary'] = {
                'total_provinces': len(new_data),
                'new_records_count': len(comparison_result['new_records']),
                'updated_records_count': len(comparison_result['updated_records']),
                'no_change_records_count': len(comparison_result['no_change_records']),
                'avg_change': self._calculate_avg_change(comparison_result['updated_records'])
            }
            
        except Exception as e:
            print(f"Lỗi khi so sánh dữ liệu: {e}")
        
        return comparison_result
    
    def get_aqi_trends(self, province: str, days: int = 7) -> Dict:
        """Phân tích xu hướng AQI"""
        historical_data = self.get_historical_aqi(province, days)
        
        if historical_data.empty:
            return {'trend': 'no_data', 'direction': 'unknown', 'change_rate': 0}
        
        # Tính xu hướng
        aqi_values = historical_data['aqi'].dropna()
        if len(aqi_values) < 2:
            return {'trend': 'insufficient_data', 'direction': 'unknown', 'change_rate': 0}
        
        # Tính hệ số tương quan với thời gian
        historical_data['date_numeric'] = pd.to_datetime(historical_data['date']).astype(int)
        correlation = historical_data['date_numeric'].corr(aqi_values)
        
        # Xác định xu hướng
        if correlation > 0.1:
            trend = 'increasing'
            direction = 'up'
        elif correlation < -0.1:
            trend = 'decreasing'
            direction = 'down'
        else:
            trend = 'stable'
            direction = 'stable'
        
        # Tính tỷ lệ thay đổi
        first_aqi = aqi_values.iloc[0]
        last_aqi = aqi_values.iloc[-1]
        change_rate = ((last_aqi - first_aqi) / first_aqi * 100) if first_aqi != 0 else 0
        
        return {
            'trend': trend,
            'direction': direction,
            'change_rate': round(change_rate, 2),
            'data_points': len(aqi_values),
            'first_aqi': first_aqi,
            'last_aqi': last_aqi
        }
    
    def get_province_ranking(self, date: Optional[str] = None) -> pd.DataFrame:
        """Xếp hạng các tỉnh theo AQI"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT province, aqi, date
                FROM daily_aqi 
                WHERE date = ?
                ORDER BY aqi ASC
            '''
            return pd.read_sql_query(query, conn, params=[date])
    
    def get_aqi_statistics(self, province: Optional[str] = None, days: int = 30) -> Dict:
        """Lấy thống kê AQI"""
        with sqlite3.connect(self.db_path) as conn:
            if province:
                query = '''
                    SELECT 
                        MIN(aqi) as min_aqi,
                        MAX(aqi) as max_aqi,
                        AVG(aqi) as avg_aqi,
                        COUNT(*) as total_records
                    FROM daily_aqi 
                    WHERE province = ? 
                    AND date >= date('now', '-{} days')
                '''.format(days)
                result = pd.read_sql_query(query, conn, params=[province])
            else:
                query = '''
                    SELECT 
                        province,
                        MIN(aqi) as min_aqi,
                        MAX(aqi) as max_aqi,
                        AVG(aqi) as avg_aqi,
                        COUNT(*) as total_records
                    FROM daily_aqi 
                    WHERE date >= date('now', '-{} days')
                    GROUP BY province
                '''.format(days)
                result = pd.read_sql_query(query, conn)
            
            return result.to_dict('records')
    
    def _update_statistics(self, aqi_data: pd.DataFrame):
        """Cập nhật thống kê AQI"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                for _, row in aqi_data.iterrows():
                    province = row['Province']
                    date = row['Date']
                    
                    # Tính thống kê cho tỉnh này
                    stats_query = '''
                        SELECT 
                            MIN(aqi) as min_aqi,
                            MAX(aqi) as max_aqi,
                            AVG(aqi) as avg_aqi,
                            COUNT(*) as total_records
                        FROM daily_aqi 
                        WHERE province = ? AND date = ?
                    '''
                    stats = pd.read_sql_query(stats_query, conn, params=[province, date])
                    
                    if not stats.empty:
                        # Lưu thống kê
                        insert_query = '''
                            INSERT OR REPLACE INTO aqi_statistics 
                            (province, date, min_aqi, max_aqi, avg_aqi, total_records)
                            VALUES (?, ?, ?, ?, ?, ?)
                        '''
                        conn.execute(insert_query, (
                            province, date,
                            stats['min_aqi'].iloc[0],
                            stats['max_aqi'].iloc[0],
                            stats['avg_aqi'].iloc[0],
                            stats['total_records'].iloc[0]
                        ))
        except Exception as e:
            print(f"Lỗi khi cập nhật thống kê: {e}")
    
    def _track_changes(self, aqi_data: pd.DataFrame):
        """Theo dõi thay đổi AQI"""
        try:
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            with sqlite3.connect(self.db_path) as conn:
                for _, row in aqi_data.iterrows():
                    province = row['Province']
                    new_aqi = row['AQI']
                    
                    # Lấy AQI cũ
                    old_query = '''
                        SELECT aqi FROM daily_aqi 
                        WHERE province = ? AND date = ?
                    '''
                    old_result = pd.read_sql_query(old_query, conn, params=[province, yesterday])
                    
                    if not old_result.empty:
                        old_aqi = old_result['aqi'].iloc[0]
                        change_amount = new_aqi - old_aqi if pd.notna(new_aqi) and pd.notna(old_aqi) else None
                        change_percentage = (change_amount / old_aqi * 100) if change_amount is not None and old_aqi != 0 else None
                        
                        # Lưu thay đổi
                        change_query = '''
                            INSERT INTO aqi_changes 
                            (province, old_aqi, new_aqi, change_amount, change_percentage, date)
                            VALUES (?, ?, ?, ?, ?, ?)
                        '''
                        conn.execute(change_query, (
                            province, old_aqi, new_aqi, change_amount, 
                            change_percentage, row['Date']
                        ))
        except Exception as e:
            print(f"Lỗi khi theo dõi thay đổi: {e}")
    
    def _calculate_avg_change(self, updated_records: List[Dict]) -> float:
        """Tính thay đổi trung bình"""
        if not updated_records:
            return 0.0
        
        changes = [record['change'] for record in updated_records if record['change'] is not None]
        return sum(changes) / len(changes) if changes else 0.0
    
    def cleanup_old_data(self, days_to_keep: int = 365):
        """Dọn dẹp dữ liệu cũ"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')
                
                # Xóa dữ liệu cũ
                conn.execute('DELETE FROM daily_aqi WHERE date < ?', (cutoff_date,))
                conn.execute('DELETE FROM hourly_aqi WHERE datetime < ?', (cutoff_date,))
                conn.execute('DELETE FROM aqi_changes WHERE date < ?', (cutoff_date,))
                conn.execute('DELETE FROM aqi_statistics WHERE date < ?', (cutoff_date,))
                
                conn.commit()
                print(f"Đã dọn dẹp dữ liệu cũ hơn {days_to_keep} ngày")
        except Exception as e:
            print(f"Lỗi khi dọn dẹp dữ liệu: {e}")

# Hàm tiện ích
def get_database_instance() -> AQIDatabase:
    """Lấy instance database"""
    return AQIDatabase()

if __name__ == "__main__":
    # Test database
    db = AQIDatabase()
    
    # Tạo dữ liệu test
    test_data = pd.DataFrame({
        'Province': ['Ha Noi', 'Ho Chi Minh City', 'Da Nang'],
        'AQI': [85, 120, 95],
        'Date': [datetime.now().strftime('%Y-%m-%d')] * 3
    })
    
    # Lưu dữ liệu
    db.save_daily_aqi(test_data)
    
    # So sánh dữ liệu
    comparison = db.compare_aqi_data(test_data)
    print("Kết quả so sánh:")
    print(comparison)
    
    # Lấy thống kê
    stats = db.get_aqi_statistics()
    print("\nThống kê:")
    print(stats)
