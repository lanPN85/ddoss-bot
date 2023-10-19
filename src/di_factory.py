from injectable import injectable_factory, autowired, Autowired
from telegram.ext import Application

from src.settings import Settings


@injectable_factory(Application, singleton=True)
@autowired
def application_factory(settings: Autowired(Settings)) -> Application:
    return (
        Application.builder()
        .token(settings.telegram_token)
        .build()
    )
