from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vibe Project Backend"
    POSTGRES_URL: str = "postgresql+asyncpg://user:password@localhost:5432/db"

    class Config:
        env_file = ".env"

settings = Settings()
