from typing import Union

from pydantic import AnyUrl, FilePath, NewPath, PositiveInt

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env_settings")

    alarm_interval_seconds: PositiveInt
    api_url: AnyUrl
    log_file_name: Union[NewPath, FilePath]
    log_file_mode: str


settings = Settings()
