from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AI Each Other"
    OPEN_AI_TOKEN: str
    OPEN_AI_MODEL: str
    BARD_AI_TOKEN: str

    class Config:
        env_file = "settings.env"
        env_prefix = ""

settings = Settings()
