import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_FILMS_USER: str
    DB_FILMS_PASSWORD: str
    DB_FILMS_NAME: str
    DB_FILMS_HOST: str
    DB_FILMS_PORT: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.env")
    )

    def get_db_url(self):
        return (f"postgresql://{self.DB_FILMS_USER}:{self.DB_FILMS_PASSWORD}@"
                f"{self.DB_FILMS_HOST}:{self.DB_FILMS_PORT}/{self.DB_FILMS_NAME}")


settings = Settings()
