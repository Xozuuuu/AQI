"""
AQI Monitoring System

A comprehensive air quality monitoring system with real-time data collection,
analysis, prediction, and reporting capabilities.

Author: AQI Monitoring Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "AQI Monitoring Team"
__email__ = "support@aqimonitoring.com"
__license__ = "MIT"

# Core modules
from .core.database import AQIDatabase
from .core.config import Settings
from .models.aqi_data import AQIData, AQIComparison
from .services.data_service import DataService
from .services.prediction_service import PredictionService
from .services.reporting_service import ReportingService

__all__ = [
    "AQIDatabase",
    "Settings", 
    "AQIData",
    "AQIComparison",
    "DataService",
    "PredictionService",
    "ReportingService",
]
