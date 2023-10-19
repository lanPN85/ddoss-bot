from telegram.ext import MessageHandler, ContextTypes, filters
from injectable import injectable, autowired, Autowired
from telegram import Update
from asyncio import Lock
from loguru import logger
from datetime import date

from src.model import MessageKey, MessageType


@injectable(singleton=True)
class MessageCounterHandler(MessageHandler):
    """Count member messages in the group chat
    """
    def __init__(self):
        super().__init__(
            filters=~filters.COMMAND,
            callback=self.callback
        )
        self.lock = Lock()

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        async with self.lock:
            post = update.message

            if post is None:
                return

            message_type = MessageType.TEXT
            if post.video is not None:
                message_type = MessageType.VIDEO
            elif post.photo is not None:
                message_type = MessageType.IMAGE

            topic_name = None
            if post.forum_topic_created is not None:
                topic_name = post.forum_topic_created.name

            key = MessageKey(
                date=date.today(),
                chat_id=post.chat.id,
                user_id=post.from_user.id,
                topic_name=topic_name,
                type_=message_type,
            )
            logger.debug(str(key))
