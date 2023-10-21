from pydantic_settings import BaseSettings
from injectable import injectable


@injectable(singleton=True)
class Settings(BaseSettings):
    bot_canon_name: str = "@tcv_ddoss_bot"

    telegram_token: str

    postgres_user: str = ""
    postgres_password: str = ""
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_database: str = "ddossbot"

    daily_award_limit: int | None = None
