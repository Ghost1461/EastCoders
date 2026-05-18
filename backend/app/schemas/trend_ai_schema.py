from pydantic import BaseModel
from typing import Optional

class TrendAISummaryResponse(BaseModel):
    market_overview: str
    personal_opportunities: str
    action_suggestions: str


class TrendAIAdviceResponse(BaseModel):
    trend_id: int
    advice: str


class TrendAIAdviceRequest(BaseModel):
    extra_note: Optional[str] = None
    force_refresh: bool = False    