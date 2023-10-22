from telegram.ext import MessageHandler, ContextTypes, filters
from injectable import injectable, autowired, Autowired
from telegram import Update
from asyncio import Lock
from loguru import logger
from datetime import date

from src.model import MessageKey, MessageType
from src.db.base import IDatabaseHelper


@injectable(singleton=True)
class MessageCounterHandler(MessageHandler):
    """Count member messages in the group chat
    """
    @autowired
    def __init__(self, db_helper: Autowired(IDatabaseHelper)):
        super().__init__(
            filters=~filters.COMMAND,
            callback=self.callback
        )
        self.db_helper: IDatabaseHelper = db_helper
        self.lock = Lock()

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        async with self.lock:
            post = update.message
            logger.debug(str(post))

            if post is None:
                return

            message_type = MessageType.TEXT
            if post.video is not None:
                message_type = MessageType.VIDEO
            elif len(post.photo) > 0:
                message_type = MessageType.IMAGE

            topic_name = None
            if post.reply_to_message is not None:
                if post.reply_to_message.forum_topic_created is not None:
                    topic_name = post.reply_to_message.forum_topic_created.name

            key = MessageKey(
                date=date.today(),
                chat_name=post.chat.title or "",
                user_name=post.from_user.name,
                topic_name=topic_name or "",
                type_=message_type,
            )

            logger.info(f"Incrementing message count for {key}")
            await self.db_helper.increment_message_count(key)
