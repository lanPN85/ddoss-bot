from pydantic_settings import BaseSettings
from injectable import injectable


@injectable(singleton=True)
class TelegramSettings(BaseSettings):
    telegram_token: str


@injectable(singleton=True)
class AwardHandlerSettings(BaseSettings):
    daily_award_limit: int | None = None


@injectable(singleton=True)
class PostgresSettings(BaseSettings):
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_database: str = "ddossbot"

    def dsn(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"


@injectable(singleton=True)
class BaseActorSettings(BaseSettings):
    active_chat_id: int | None = None


@injectable(singleton=True)
class MemeActorSettings(BaseActorSettings):
    meme_thread_id: int | None = None
