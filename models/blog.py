from main import get_db
from database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func

class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    
    created_at = Column(DateTime, default=func.now(),nullable=False)
    updated_at = Column(DateTime, default=func.now(),onupdate=func.now(),nullable=False)
    