"""
Data service for AQI data operations.

This service handles all data-related operations including fetching,
processing, and storing AQI data.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..core.config import get_settings
from ..core.database import AQIDatabase
from ..models.aqi_data import AQIData, AQIComparison, AQITrend, AQIStatistics, AQIRanking

logger = logging.getLogger(__name__)


class DataService:
    """Service for AQI data operations."""
    
    def __init__(self):
        self.settings = get_settings()
        self.db = AQIDatabase()
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create HTTP session with retry strategy."""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=self.settings.api.retry_attempts,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    async def fetch_aqi_data(self) -> List[AQIData]:
        """Fetch AQI data from API."""
        logger.info("Fetching AQI data from API")
        
        aqi_data = []
        for province_code in self.settings.provinces:
            try:
                data = await self._fetch_province_aqi(province_code)
                if data:
                    aqi_data.append(data)
            except Exception as e:
                logger.error(f"Error fetching data for {province_code}: {e}")
                continue
        
        logger.info(f"Fetched {len(aqi_data)} AQI records")
        return aqi_data
    
    async def _fetch_province_aqi(self, province_code: str) -> Optional[AQIData]:
        """Fetch AQI data for a specific province."""
        url = f"{self.settings.api.base_url}/feed/{province_code}/"
        params = {"token": self.settings.api.key}
        
        try:
            response = self.session.get(
                url, 
                params=params, 
                timeout=self.settings.api.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') == 'ok' and isinstance(data.get('data'), dict):
                aqi = data['data'].get('aqi')
                if aqi in ('-', None, ''):
                    aqi = None
                    logger.warning(f"No AQI data for {province_code}")
                else:
                    aqi = int(aqi)
            else:
                aqi = None
                logger.warning(f"Invalid response for {province_code}")
            
            province_name = self.settings.get_province_name(province_code)
            
            return AQIData(
                province=province_name,
                aqi=aqi,
                date=datetime.now()
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {province_code}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {province_code}: {e}")
            return None
    
    def save_aqi_data(self, aqi_data: List[AQIData]) -> bool:
        """Save AQI data to database."""
        logger.info(f"Saving {len(aqi_data)} AQI records to database")
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame([data.dict() for data in aqi_data])
            df['Date'] = df['date']
            df = df.drop('date', axis=1)
            
            success = self.db.save_daily_aqi(df)
            
            if success:
                logger.info("Successfully saved AQI data to database")
            else:
                logger.error("Failed to save AQI data to database")
            
            return success
            
        except Exception as e:
            logger.error(f"Error saving AQI data: {e}")
            return False
    
    def get_latest_aqi_data(self, province: Optional[str] = None) -> List[AQIData]:
        """Get latest AQI data."""
        logger.info(f"Getting latest AQI data for {province or 'all provinces'}")
        
        try:
            df = self.db.get_latest_aqi(province)
            
            if df.empty:
                logger.warning("No AQI data found")
                return []
            
            aqi_data = []
            for _, row in df.iterrows():
                aqi_data.append(AQIData(
                    province=row['province'],
                    aqi=row['aqi'],
                    date=pd.to_datetime(row['date'])
                ))
            
            logger.info(f"Retrieved {len(aqi_data)} AQI records")
            return aqi_data
            
        except Exception as e:
            logger.error(f"Error getting latest AQI data: {e}")
            return []
    
    def get_historical_aqi_data(self, province: str, days: int = 30) -> List[AQIData]:
        """Get historical AQI data."""
        logger.info(f"Getting historical AQI data for {province} ({days} days)")
        
        try:
            df = self.db.get_historical_aqi(province, days)
            
            if df.empty:
                logger.warning(f"No historical data found for {province}")
                return []
            
            aqi_data = []
            for _, row in df.iterrows():
                aqi_data.append(AQIData(
                    province=row['province'],
                    aqi=row['aqi'],
                    date=pd.to_datetime(row['date'])
                ))
            
            logger.info(f"Retrieved {len(aqi_data)} historical AQI records")
            return aqi_data
            
        except Exception as e:
            logger.error(f"Error getting historical AQI data: {e}")
            return []
    
    def compare_aqi_data(self, new_data: List[AQIData]) -> List[AQIComparison]:
        """Compare new AQI data with previous data."""
        logger.info("Comparing AQI data")
        
        try:
            # Convert to DataFrame for comparison
            df = pd.DataFrame([data.dict() for data in new_data])
            df['Date'] = df['date']
            df = df.drop('date', axis=1)
            
            comparison_result = self.db.compare_aqi_data(df)
            
            comparisons = []
            for record in comparison_result['updated_records']:
                comparisons.append(AQIComparison(
                    province=record['province'],
                    old_aqi=record['old_aqi'],
                    new_aqi=record['new_aqi'],
                    change_amount=record['change'],
                    change_percentage=record['change_percentage'],
                    date=datetime.now()
                ))
            
            logger.info(f"Created {len(comparisons)} AQI comparisons")
            return comparisons
            
        except Exception as e:
            logger.error(f"Error comparing AQI data: {e}")
            return []
    
    def get_aqi_trends(self, province: str, days: int = 7) -> AQITrend:
        """Get AQI trends for a province."""
        logger.info(f"Getting AQI trends for {province} ({days} days)")
        
        try:
            trend_data = self.db.get_aqi_trends(province, days)
            
            return AQITrend(
                province=province,
                trend=trend_data['trend'],
                direction=trend_data['direction'],
                change_rate=trend_data['change_rate'],
                data_points=trend_data['data_points'],
                first_aqi=trend_data.get('first_aqi'),
                last_aqi=trend_data.get('last_aqi'),
                period_days=days
            )
            
        except Exception as e:
            logger.error(f"Error getting AQI trends: {e}")
            return AQITrend(
                province=province,
                trend="no_data",
                direction="unknown",
                change_rate=0.0,
                data_points=0,
                period_days=days
            )
    
    def get_aqi_statistics(self, province: Optional[str] = None, days: int = 30) -> List[AQIStatistics]:
        """Get AQI statistics."""
        logger.info(f"Getting AQI statistics for {province or 'all provinces'} ({days} days)")
        
        try:
            stats_data = self.db.get_aqi_statistics(province, days)
            
            statistics = []
            for stat in stats_data:
                statistics.append(AQIStatistics(
                    province=stat['province'],
                    min_aqi=stat['min_aqi'],
                    max_aqi=stat['max_aqi'],
                    avg_aqi=stat['avg_aqi'],
                    median_aqi=stat.get('median_aqi'),
                    std_aqi=stat.get('std_aqi'),
                    total_records=stat['total_records'],
                    date=datetime.now()
                ))
            
            logger.info(f"Retrieved {len(statistics)} AQI statistics")
            return statistics
            
        except Exception as e:
            logger.error(f"Error getting AQI statistics: {e}")
            return []
    
    def get_aqi_ranking(self, date: Optional[datetime] = None) -> List[AQIRanking]:
        """Get AQI ranking."""
        logger.info("Getting AQI ranking")
        
        try:
            date_str = date.strftime('%Y-%m-%d') if date else None
            df = self.db.get_province_ranking(date_str)
            
            if df.empty:
                logger.warning("No ranking data found")
                return []
            
            rankings = []
            for i, (_, row) in enumerate(df.iterrows(), 1):
                rankings.append(AQIRanking(
                    rank=i,
                    province=row['province'],
                    aqi=row['aqi'],
                    date=pd.to_datetime(row['date'])
                ))
            
            logger.info(f"Retrieved {len(rankings)} AQI rankings")
            return rankings
            
        except Exception as e:
            logger.error(f"Error getting AQI ranking: {e}")
            return []
    
    async def fetch_and_save_aqi_data(self) -> tuple[List[AQIData], List[AQIComparison]]:
        """Fetch and save AQI data, return data and comparisons."""
        logger.info("Fetching and saving AQI data")
        
        # Fetch data
        aqi_data = await self.fetch_aqi_data()
        
        if not aqi_data:
            logger.warning("No AQI data fetched")
            return [], []
        
        # Save data
        success = self.save_aqi_data(aqi_data)
        
        if not success:
            logger.error("Failed to save AQI data")
            return aqi_data, []
        
        # Compare data
        comparisons = self.compare_aqi_data(aqi_data)
        
        logger.info(f"Successfully processed {len(aqi_data)} AQI records with {len(comparisons)} comparisons")
        return aqi_data, comparisons
    
    def cleanup_old_data(self, days_to_keep: int = 365) -> bool:
        """Cleanup old data."""
        logger.info(f"Cleaning up data older than {days_to_keep} days")
        
        try:
            self.db.cleanup_old_data(days_to_keep)
            logger.info("Successfully cleaned up old data")
            return True
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return False
