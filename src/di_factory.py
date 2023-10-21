from injectable import injectable_factory, autowired, Autowired
from telegram.ext import Application

from src.db.base import IDatabaseHelper
from src.db.postgres import PostgresDatabaseHelper
from src.settings import Settings


@injectable_factory(Application, singleton=True)
@autowired
def application_factory(settings: Autowired(Settings)) -> Application:
    return Application.builder().token(settings.telegram_token).build()


@injectable_factory(IDatabaseHelper, singleton=True)
@autowired
def db_factory(settings: Autowired(Settings)) -> IDatabaseHelper:
    return PostgresDatabaseHelper(
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"
    )
