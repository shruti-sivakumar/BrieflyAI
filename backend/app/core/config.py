from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379"

    # Supabase Auth
    SUPABASE_JWT_SECRET: str

    class Config:
        env_file = ".env"

settings = Settings()