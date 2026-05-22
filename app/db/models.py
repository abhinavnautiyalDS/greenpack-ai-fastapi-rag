from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import Base


class Declaration(Base):
    __tablename__ = "declarations"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String, unique=True)
    producer_id = Column(String)
    month = Column(String)

    rigid_plastic = Column(Float)
    flexible_plastic = Column(Float)
    multilayer_plastic = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)