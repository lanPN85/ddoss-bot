from pydantic_settings import BaseSettings
from injectable import injectable


@injectable(singleton=True)
class Settings(BaseSettings):
    telegram_token: str
