from datetime import timedelta
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Envrionment(str, Enum):
    TEST = "TEST"
    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"


class Setting(BaseSettings):
    TITLE: str = "Github pokemon collection api"
    VERSION: str = "4"

    ENVIRONMENT: Envrionment = Envrionment.PRODUCTION

    DATABASE_URL: str
    GITHUB_API_TOKEN: str

    SVG_WIDTH: int = 300
    SVG_MIN_WIDTH: int = 250
    SVG_HEIGHT: int = 250
    SVG_MIN_HEIGHT: int = 200
    POKEMON_PER_COMMIT_POINT: int = 100
    SHINY_POKEMON_RATE: float = 0.1
    COMMIT_POINT_UPDATE_PERIOD: timedelta = timedelta(hours=1)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Setting()  # type: ignore
