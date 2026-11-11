from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class HotspotBase(BaseModel):
    title: str
    category: str
    heat_score: float  # 0-100
    source: str
    url: Optional[str] = None


class HotspotCreate(HotspotBase):
    pass


class HotspotResponse(HotspotBase):
    id: int
    created_at: datetime
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    ai_summary: Optional[str] = None

    class Config:
        from_attributes = True


class HotspotList(BaseModel):
    items: List[HotspotResponse]
    total: int


class AIAnalysisRequest(BaseModel):
    text: str
    topic: str


class AIAnalysisResponse(BaseModel):
    sentiment: str  # positive, neutral, negative
    sentiment_score: float  # -1 to 1
    summary: str
    keywords: List[str]
    prediction: str


class TrendDataPoint(BaseModel):
    date: str
    heat_score: float
    topic_count: int


class CategoryStat(BaseModel):
    category: str
    count: int
    avg_heat: float