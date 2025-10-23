"""
Configuration management for AQI Monitoring System.

This module provides centralized configuration management using Pydantic
for validation and type safety.
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field, validator
from pathlib import Path


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    host: str = Field(default="localhost", env="DB_HOST")
    port: int = Field(default=5432, env="DB_PORT")
    name: str = Field(default="aqi_monitoring", env="DB_NAME")
    user: str = Field(default="aqi_user", env="DB_USER")
    password: str = Field(default="aqi_password", env="DB_PASSWORD")
    url: Optional[str] = Field(default=None, env="DATABASE_URL")
    
    @validator('url', pre=True, always=True)
    def build_database_url(cls, v, values):
        """Build database URL from individual components."""
        if v:
            return v
        return f"postgresql://{values['user']}:{values['password']}@{values['host']}:{values['port']}/{values['name']}"


class APIConfig(BaseSettings):
    """API configuration."""
    
    key: str = Field(..., env="API_KEY")
    base_url: str = Field(default="https://api.waqi.info", env="API_BASE_URL")
    timeout: int = Field(default=30, env="API_TIMEOUT")
    retry_attempts: int = Field(default=3, env="API_RETRY_ATTEMPTS")
    rate_limit: int = Field(default=100, env="API_RATE_LIMIT")


class AppConfig(BaseSettings):
    """Application configuration."""
    
    name: str = Field(default="AQI Monitoring System", env="APP_NAME")
    version: str = Field(default="1.0.0", env="APP_VERSION")
    debug: bool = Field(default=False, env="DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    max_workers: int = Field(default=4, env="MAX_WORKERS")
    secret_key: str = Field(..., env="SECRET_KEY")
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()


class MonitoringConfig(BaseSettings):
    """Monitoring configuration."""
    
    enabled: bool = Field(default=True, env="ENABLE_MONITORING")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    health_check_interval: int = Field(default=60, env="HEALTH_CHECK_INTERVAL")
    alert_threshold: int = Field(default=150, env="ALERT_THRESHOLD")


class DataConfig(BaseSettings):
    """Data configuration."""
    
    raw_data_path: Path = Field(default=Path("data/raw"), env="RAW_DATA_PATH")
    processed_data_path: Path = Field(default=Path("data/processed"), env="PROCESSED_DATA_PATH")
    export_path: Path = Field(default=Path("data/exports"), env="EXPORT_PATH")
    backup_retention_days: int = Field(default=365, env="BACKUP_RETENTION_DAYS")
    
    @validator('raw_data_path', 'processed_data_path', 'export_path')
    def create_directories(cls, v):
        """Create directories if they don't exist."""
        v.mkdir(parents=True, exist_ok=True)
        return v


class Settings(BaseSettings):
    """Main settings class."""
    
    # Sub-configurations
    database: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()
    app: AppConfig = AppConfig()
    monitoring: MonitoringConfig = MonitoringConfig()
    data: DataConfig = DataConfig()
    
    # Project settings
    project_root: Path = Field(default=Path.cwd(), env="PROJECT_ROOT")
    provinces: List[str] = Field(default_factory=lambda: [
        'hanoi', '@11593', 'thai-nguyen', 'viet-tri', '@12959',
        'bac-ninh', 'hung-yen', '@14641', '@13013', '@13672',
        '@5499', '@13028', 'hue', 'da-nang', 'gia-lai',
        'nha-trang', 'A476452', '@13659', 'vung-tau', 'vinh-long',
        '@13662', 'can-tho'
    ])
    
    province_mapping: dict = Field(default_factory=lambda: {
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
    })
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def get_province_name(self, province_code: str) -> str:
        """Get province name from code."""
        return self.province_mapping.get(province_code, province_code)
    
    def get_province_codes(self) -> List[str]:
        """Get all province codes."""
        return self.provinces
    
    def get_province_names(self) -> List[str]:
        """Get all province names."""
        return list(self.province_mapping.values())


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance."""
    return settings
