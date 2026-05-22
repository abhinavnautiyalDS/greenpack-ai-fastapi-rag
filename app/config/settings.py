from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  
    DATABASE_URL: str
    COHERE_API_KEY: str
    GROK_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()