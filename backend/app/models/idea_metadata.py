from sqlalchemy import Column, Integer, Text, ForeignKey, Float, ARRAY
from sqlalchemy.orm import relationship
from app.models.idea import Base

class IdeaMetadata(Base):
    __tablename__ = "idea_metadata"

    id = Column(Integer, primary_key=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), unique=True)

    summary = Column(Text)
    keywords = Column(ARRAY(Text))
    tech_stack = Column(ARRAY(Text))
    difficulty = Column(Integer)
    category = Column(Text)
    quality_score = Column(Float)

    idea = relationship("Idea", backref="metadata")
