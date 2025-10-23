"""
Data models for AQI data.

This module defines Pydantic models for AQI data validation and serialization.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class AQICategory(str, Enum):
    """AQI categories based on air quality index."""
    
    GOOD = "good"
    MODERATE = "moderate"
    UNHEALTHY_FOR_SENSITIVE = "unhealthy_for_sensitive"
    UNHEALTHY = "unhealthy"
    VERY_UNHEALTHY = "very_unhealthy"
    HAZARDOUS = "hazardous"
    UNKNOWN = "unknown"


class AQIData(BaseModel):
    """AQI data model."""
    
    province: str = Field(..., description="Province name")
    aqi: Optional[int] = Field(None, ge=0, le=500, description="Air Quality Index")
    date: datetime = Field(..., description="Date of measurement")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, description="Creation timestamp")
    
    @validator('aqi')
    def validate_aqi(cls, v):
        """Validate AQI value."""
        if v is not None and (v < 0 or v > 500):
            raise ValueError("AQI must be between 0 and 500")
        return v
    
    @property
    def category(self) -> AQICategory:
        """Get AQI category."""
        if self.aqi is None:
            return AQICategory.UNKNOWN
        elif self.aqi <= 50:
            return AQICategory.GOOD
        elif self.aqi <= 100:
            return AQICategory.MODERATE
        elif self.aqi <= 150:
            return AQICategory.UNHEALTHY_FOR_SENSITIVE
        elif self.aqi <= 200:
            return AQICategory.UNHEALTHY
        elif self.aqi <= 300:
            return AQICategory.VERY_UNHEALTHY
        else:
            return AQICategory.HAZARDOUS
    
    @property
    def category_name(self) -> str:
        """Get AQI category name in Vietnamese."""
        category_names = {
            AQICategory.GOOD: "Tốt",
            AQICategory.MODERATE: "Trung bình",
            AQICategory.UNHEALTHY_FOR_SENSITIVE: "Không tốt cho nhóm nhạy cảm",
            AQICategory.UNHEALTHY: "Không tốt",
            AQICategory.VERY_UNHEALTHY: "Rất không tốt",
            AQICategory.HAZARDOUS: "Nguy hiểm",
            AQICategory.UNKNOWN: "Không có dữ liệu"
        }
        return category_names[self.category]
    
    @property
    def color(self) -> str:
        """Get color code for AQI category."""
        colors = {
            AQICategory.GOOD: "#00e400",
            AQICategory.MODERATE: "#ffff00",
            AQICategory.UNHEALTHY_FOR_SENSITIVE: "#ff7e00",
            AQICategory.UNHEALTHY: "#ff0000",
            AQICategory.VERY_UNHEALTHY: "#8f3f97",
            AQICategory.HAZARDOUS: "#7e0023",
            AQICategory.UNKNOWN: "#808080"
        }
        return colors[self.category]
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AQIComparison(BaseModel):
    """AQI comparison data model."""
    
    province: str = Field(..., description="Province name")
    old_aqi: Optional[int] = Field(None, description="Previous AQI value")
    new_aqi: Optional[int] = Field(None, description="Current AQI value")
    change_amount: Optional[int] = Field(None, description="Change in AQI")
    change_percentage: Optional[float] = Field(None, description="Percentage change")
    date: datetime = Field(..., description="Comparison date")
    
    @validator('change_amount', pre=True, always=True)
    def calculate_change_amount(cls, v, values):
        """Calculate change amount."""
        if v is not None:
            return v
        old_aqi = values.get('old_aqi')
        new_aqi = values.get('new_aqi')
        if old_aqi is not None and new_aqi is not None:
            return new_aqi - old_aqi
        return None
    
    @validator('change_percentage', pre=True, always=True)
    def calculate_change_percentage(cls, v, values):
        """Calculate change percentage."""
        if v is not None:
            return v
        old_aqi = values.get('old_aqi')
        new_aqi = values.get('new_aqi')
        if old_aqi is not None and new_aqi is not None and old_aqi != 0:
            return ((new_aqi - old_aqi) / old_aqi) * 100
        return None
    
    @property
    def change_type(self) -> str:
        """Get change type."""
        if self.change_amount is None:
            return "unknown"
        elif self.change_amount > 0:
            return "increased"
        elif self.change_amount < 0:
            return "decreased"
        else:
            return "unchanged"
    
    @property
    def significance(self) -> str:
        """Get change significance."""
        if self.change_percentage is None:
            return "unknown"
        elif abs(self.change_percentage) >= 20:
            return "significant"
        elif abs(self.change_percentage) >= 10:
            return "moderate"
        elif abs(self.change_percentage) >= 5:
            return "minor"
        else:
            return "negligible"


class AQITrend(BaseModel):
    """AQI trend analysis model."""
    
    province: str = Field(..., description="Province name")
    trend: str = Field(..., description="Trend direction")
    direction: str = Field(..., description="Trend direction")
    change_rate: float = Field(..., description="Change rate percentage")
    data_points: int = Field(..., description="Number of data points")
    first_aqi: Optional[int] = Field(None, description="First AQI value")
    last_aqi: Optional[int] = Field(None, description="Last AQI value")
    period_days: int = Field(..., description="Analysis period in days")
    
    @property
    def trend_description(self) -> str:
        """Get trend description in Vietnamese."""
        descriptions = {
            "increasing": "Tăng",
            "decreasing": "Giảm", 
            "stable": "Ổn định",
            "no_data": "Không có dữ liệu",
            "insufficient_data": "Dữ liệu không đủ"
        }
        return descriptions.get(self.trend, "Không xác định")


class AQIStatistics(BaseModel):
    """AQI statistics model."""
    
    province: str = Field(..., description="Province name")
    min_aqi: Optional[int] = Field(None, description="Minimum AQI")
    max_aqi: Optional[int] = Field(None, description="Maximum AQI")
    avg_aqi: Optional[float] = Field(None, description="Average AQI")
    median_aqi: Optional[float] = Field(None, description="Median AQI")
    std_aqi: Optional[float] = Field(None, description="Standard deviation")
    total_records: int = Field(..., description="Total number of records")
    date: datetime = Field(..., description="Statistics date")
    
    @property
    def aqi_range(self) -> Optional[int]:
        """Get AQI range."""
        if self.min_aqi is not None and self.max_aqi is not None:
            return self.max_aqi - self.min_aqi
        return None
    
    @property
    def variability(self) -> str:
        """Get variability description."""
        if self.std_aqi is None:
            return "unknown"
        elif self.std_aqi <= 10:
            return "low"
        elif self.std_aqi <= 25:
            return "moderate"
        else:
            return "high"


class AQIRanking(BaseModel):
    """AQI ranking model."""
    
    rank: int = Field(..., description="Rank position")
    province: str = Field(..., description="Province name")
    aqi: int = Field(..., description="AQI value")
    date: datetime = Field(..., description="Ranking date")
    
    @property
    def rank_description(self) -> str:
        """Get rank description."""
        if self.rank == 1:
            return "Tốt nhất"
        elif self.rank <= 3:
            return "Tốt"
        elif self.rank <= 10:
            return "Trung bình"
        else:
            return "Cần cải thiện"
