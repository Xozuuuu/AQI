from decouple import config

API_KEY = config('API_KEY')
PROVINCES_LIST = [
    'hanoi',
    '@11593',
    'thai-nguyen',
    'viet-tri',
    '@12959',
    'bac-ninh',
    'hung-yen',
    '@14641',
    '@13013',
    '@13672',
    '@5499',
    '@13028',
    'hue',
    'da-nang',
    'gia-lai',
    'nha-trang',
    'A476452',
    '@13659',
    'vung-tau',
    'vinh-long',
    '@13662',
    'can-tho'
]  # Mở rộng sau (slug API)
PROVINCE_MAPPING = {
    'hanoi': 'Ha Noi',
    '@11593': 'Ho Chi Minh City',
    'thai-nguyen': 'Thai Nguyen',
    'viet-tri': 'Viet Tri',
    '@12959': 'Bac Giang',
    'bac-ninh': 'Bac Ninh',
    'hung-yen': 'Hung Yen',
    '@14641': 'Thai Binh',
    '@13013': 'Ha Nam',
    '@13672': 'Ninh Binh',
    '@5499': 'Quang Ninh',
    '@13028': 'Quang Binh',
    'hue': 'Thua Thien Hue',
    'da-nang': 'Da Nang',
    'gia-lai': 'Gia Lai',
    'nha-trang': 'Nha Trang',
    'A476452': 'Lam Dong',
    '@13659': 'Tay Ninh',
    'vung-tau': 'Vung Tau',
    'vinh-long': 'Vinh Long',
    '@13662': 'Tra Vinh',
    'can-tho': 'Can Tho'
}
DATA_PATH = 'data/processed/vn_pollution.geojson'
DB_PATH = 'data/processed/aqi_history.db'