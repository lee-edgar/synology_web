from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CareerBase(BaseModel):
    title: str
    company: str
    company_type: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
    files: List[str] = []

class CareerCreate(CareerBase):
    pass

class Career(CareerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
