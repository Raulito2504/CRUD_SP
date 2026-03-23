from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_SERVER: str
    DB_NAME:   str
    DB_USER:   str
    DB_PASS:   str = ""

    model_config = {"env_file": ".env"}


settings = Settings()
