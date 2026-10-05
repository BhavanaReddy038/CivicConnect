from backend.core.config import settings
from ai.classification.categories import CIVIC_CATEGORIES

from google import genai


client = (
    genai.Client(
        api_key=settings.GEMINI_API_KEY
    )
    if settings.GEMINI_API_KEY
    else None
)


def classify_text(text: str) -> dict:

    if client is None:
        return {
            "category": "OTHER",
            "severity": "MEDIUM",
            "confidence": 0.0,
        }

    categories = ", ".join(CIVIC_CATEGORIES)

    prompt = f"""
You are a civic complaint classification system.

Classify the following complaint.

Allowed categories:
{categories}

Return ONLY JSON:

{{
    "category": "category_name",
    "severity": "LOW|MEDIUM|HIGH|CRITICAL",
    "confidence": 0.0
}}

Complaint:
{text}
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
    )

    import json

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "category": "OTHER",
            "severity": "MEDIUM",
            "confidence": 0.0,
        }