import logging

from injectable import load_injection_container, autowired, Autowired
from loguru import logger
from telegram.constants import UpdateType
from telegram.ext import Application, BaseHandler


@autowired
def main(application: Autowired(Application), handlers: Autowired(list[BaseHandler])):
    application: Application = application
    logging.getLogger("httpx").setLevel(logging.WARNING)

    application.add_handlers(handlers)

    logger.info("Running bot...")
    application.run_polling(
        allowed_updates=[
            UpdateType.CHANNEL_POST,
            UpdateType.MESSAGE,
        ]
    )


if __name__ == "__main__":
    load_injection_container()
    main()
