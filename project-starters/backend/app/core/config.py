from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PPAI Project"
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:4200", "http://localhost:8100"]

    class Config:
        env_file = ".env"

settings = Settings()
