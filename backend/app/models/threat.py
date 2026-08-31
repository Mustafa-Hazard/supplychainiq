from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime, timezone
from app.database import Base

class Threat(Base):
    __tablename__ = "threats"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)
    external_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(Text)
    indicators = Column(Text)
    tags = Column(Text)
    priority_score = Column(Float, default=0.0, index=True)
    published_at = Column(DateTime, nullable=True)
    pulled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
