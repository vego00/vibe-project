from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vibe Project Backend"

    DATABASE_URL: str  # 기본값 없음 → 반드시 .env에서 로드됨

    class Config:
        env_file = ".env"

settings = Settings()
