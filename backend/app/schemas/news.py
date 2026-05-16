from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NewsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    image_url: Optional[str]
    source: Optional[str]
    url: str
    category: str
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class NewsDetailResponse(NewsResponse):
    pass


