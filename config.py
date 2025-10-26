from decouple import config

API_KEY = config('API_KEY')
PROVINCES_LIST = [
    'hanoi',
    '@11593',
    'thai-nguyen',
    'viet-tri',
    'bac-ninh',
    '@14641',
    '@13672',
    '@5499',
    '@13028',
    # 'hue',
    # 'da-nang',
    # 'gia-lai',
    # 'nha-trang',
    # '@13659',
    # 'vung-tau',
    # 'vinh-long',
    # '@13662',
    # 'can-tho'
]  # Mở rộng sau (slug API)
PROVINCE_MAPPING = {
    'hanoi': 'Hà Nội',
    '@11593': 'Hồ Chí Minh',
    'thai-nguyen': 'Thái Nguyên',
    'viet-tri': 'Việt Trì',
    'bac-ninh': 'Bắc Ninh',
    '@14641': 'Thái Bình',
    '@13672': 'Ninh Bình',
    '@5499': 'Quảng Ninh',
    '@13028': 'Quảng Bình',
    # 'hue': 'Thừa Thiên Huế',
    # 'da-nang': 'Đà Nẵng',
    # 'gia-lai': 'Gia Lai',
    # 'nha-trang': 'Nha Trang',
    # '@13659': 'Tây Ninh',
    # 'vung-tau': 'Vũng Tàu',
    # 'vinh-long': 'Vĩnh Long',
    # '@13662': 'Trà Vinh',
    # 'can-tho': 'Cần Thơ'
}
DATA_PATH = 'data/processed/vn_pollution.geojson'
DB_PATH = 'data/processed/aqi_history.db'