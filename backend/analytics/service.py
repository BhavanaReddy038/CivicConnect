from typing import List, Dict, Any

class AnalyticsService:
    @staticmethod
    def generate_heatmap_points() -> List[Dict[str, Any]]:
        return [
            {"latitude": 17.3850, "longitude": 78.4867, "intensity": 0.8},
            {"latitude": 17.3871, "longitude": 78.4890, "intensity": 0.5},
            {"latitude": 17.3912, "longitude": 78.4735, "intensity": 0.9}
        ]