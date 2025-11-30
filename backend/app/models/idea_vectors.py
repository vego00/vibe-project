from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.models.idea import Base

class IdeaVector(Base):
    __tablename__ = "idea_vectors"

    id = Column(Integer, primary_key=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))

    summary_vector = Column(Vector(1536))
    keyword_vector = Column(Vector(1536))
    tech_vector = Column(Vector(1536))
    combined_vector = Column(Vector(1536))

    idea = relationship("Idea", backref="vectors")
