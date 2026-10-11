from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from backend.analytics.repository import AnalyticsRepository
from backend.analytics.service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Civic Analytics"])

@router.get("/heatmap")
def get_heatmap_data():
    return AnalyticsService.generate_heatmap_points()

@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    return AnalyticsRepository.get_overview_metrics(db)