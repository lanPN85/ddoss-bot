import logging

from injectable import load_injection_container, autowired, Autowired
from loguru import logger
from telegram.constants import UpdateType
from telegram.ext import Application, BaseHandler


@autowired
def main(application: Autowired(Application), handlers: Autowired(list[BaseHandler])):
    application: Application = application
    logging.getLogger("httpx").setLevel(logging.WARNING)

    for i, handler in enumerate(handlers):
        logger.info(f"Adding handler {handler.__class__.__name__}")
        application.add_handler(handler, group=i + 1)

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
