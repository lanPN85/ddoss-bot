from injectable import injectable_factory, autowired, Autowired
from telegram.ext import Application, ExtBot

from src.settings import TelegramSettings


@injectable_factory(ExtBot, singleton=True)
@autowired
def bot_factory(settings: Autowired(TelegramSettings)) -> ExtBot:
    return ExtBot(token=settings.telegram_token)


@injectable_factory(Application, singleton=True)
@autowired
def application_factory(settings: Autowired(TelegramSettings)) -> Application:
    return Application.builder().token(settings.telegram_token).build()
