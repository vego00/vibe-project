from app.core.db import engine
from app.models.idea import Base
from app.models.idea_metadata import IdeaMetadata
from app.models.idea_vectors import IdeaVector

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
