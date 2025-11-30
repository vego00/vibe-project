from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vibe Project Backend"

    DATABASE_URL: str  # 기본값 없음 → 반드시 .env에서 로드됨

    SOLAR_API_KEY: str
    SOLAR_API_URL: str
    SOLAR_MODEL: str

    class Config:
        env_file = ".env"

settings = Settings()
