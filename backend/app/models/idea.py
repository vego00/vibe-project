from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    raw_text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())
