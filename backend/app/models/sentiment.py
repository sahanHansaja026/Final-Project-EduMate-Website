from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analyses"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)