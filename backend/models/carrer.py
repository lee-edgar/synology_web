from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from backend.models.base import Base

class Career(Base):
    __tablename__ = "careers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    company = Column(String(200), nullable=False)
    company_type = Column(String(50))
    start_date = Column(String(50), nullable=False)
    end_date = Column(String(50))
    location = Column(String(200))
    description = Column(Text)
    tags = Column(String(500))  # JSON string으로 저장
    files = Column(Text)  # JSON string으로 저장
    created_at = Column(DateTime(timezone=True), server_default=func.now())

