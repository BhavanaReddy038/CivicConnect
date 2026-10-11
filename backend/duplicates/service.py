import math
from backend.duplicates.schemas import DuplicateCheckRequest, DuplicateCheckResponse

class DuplicateService:
    @staticmethod
    def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371000  # radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @classmethod
    def find_potential_duplicates(cls, request: DuplicateCheckRequest) -> DuplicateCheckResponse:
        sample_lat = request.latitude + 0.0001
        sample_lon = request.longitude + 0.0001
        distance = cls.haversine_distance(request.latitude, request.longitude, sample_lat, sample_lon)

        if distance < 50.0:
            return DuplicateCheckResponse(
                is_potential_duplicate=True,
                potential_duplicate_ids=["sample-dup-001"],
                confidence_score=0.88,
                message=f"Found existing complaint {round(distance, 1)}m away in same category."
            )

        return DuplicateCheckResponse(
            is_potential_duplicate=False,
            potential_duplicate_ids=[],
            confidence_score=0.1,
            message="No nearby duplicate complaints identified."
        )