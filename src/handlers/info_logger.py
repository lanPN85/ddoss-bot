from telegram.ext import MessageHandler, ContextTypes, filters
from injectable import injectable, autowired, Autowired
from telegram import Update
from loguru import logger


@injectable(singleton=True)
class MessageInfoLoggerHandler(MessageHandler):
    """Count member messages in the group chat
    """
    def __init__(self):
        super().__init__(
            filters=filters.ALL,
            callback=self.callback
        )

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        logger.info(update.to_json())
