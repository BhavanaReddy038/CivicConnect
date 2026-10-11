from pydantic import BaseModel
from typing import List, Dict

class HeatmapPoint(BaseModel):
    latitude: float
    longitude: float
    intensity: float  # Scale 0.0 to 1.0 based on severity/density
    category: str

class CivicAnalyticsOverview(BaseModel):
    total_reported: int
    total_resolved: int
    community_verified_count: int
    resolution_rate_percentage: float
    category_breakdown: Dict[str, int]