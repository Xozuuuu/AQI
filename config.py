from decouple import config

API_KEY = config('API_KEY')
PROVINCES_LIST = [
    'hanoi', 
    'ho-chi-minh-city', 
    'danang'
]  # Mở rộng sau (slug API)
PROVINCE_MAPPING = {
    'hanoi': 'Ha Noi', 
    'ho-chi-minh-city': 'Ho Chi Minh City', 
    'danang': 'Da Nang'
}
DATA_PATH = 'data/processed/vn_pollution.geojson'
DB_PATH = 'data/processed/aqi_history.db'