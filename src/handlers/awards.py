from telegram.ext import filters, ContextTypes, MessageHandler
from injectable import injectable, autowired, Autowired
from telegram import Update, MessageEntity
from asyncio import Lock
from loguru import logger
from datetime import date

from src.db.base import IDatabaseHelper
from src.model import Award, AwardType


class AwardCommandHandler(MessageHandler):
    """Responds to award command
    """
    @autowired
    def __init__(self, bot_name: str, db_helper: Autowired(IDatabaseHelper)):
        super().__init__(
            filters=filters.ALL,
            callback=self.callback
        )
        self.bot_name = bot_name
        self.db_helper: IDatabaseHelper = db_helper

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # logger.debug(update.to_json())
        award = self._parse_update(update)

        if award is None:
            return

        logger.debug(str(award))

        if award.to_user == award.from_user:
            await update.message.reply_text(
                "Tự cho mình phiếu bé ngoan?? Cút."
            )
            return

        # TODO write to db

        await update.message.reply_text(
            f"Ghi nhận phiếu {'bé ngoan' if award.type_ == AwardType.UPVOTE else 'bé hư'} từ {award.from_user} đến {award.to_user}\n```{award.message}```", parse_mode="Markdown"
        )

    def _parse_update(self, update: Update) -> Award | None:
        if update.message is None:
            return None

        # Get name of the source user
        from_user = update.message.from_user.name
        chat_name = update.message.chat.title

        # Get award type
        award_type = None
        if "/aw +1 " in update.message.text:
            award_type = AwardType.UPVOTE
        elif "/aw -1 " in update.message.text:
            award_type = AwardType.DOWNVOTE
        else:
            return None

        mentions = update.message.parse_entities(types=[MessageEntity.MENTION])
        logger.debug(str(mentions))

        # Find to_user
        to_user: str | None = None

        # TODO remove this
        to_user = "lanpn"

        for entity, text in mentions.items():
            if entity.user is None:
                continue
            to_user = entity.user.name

        if to_user is None:
            return None

        # Find the award message
        message = ""
        command_offset = update.message.text.find("/aw")
        if command_offset != -1:
            message = update.message.text[command_offset + 4:]

        return Award(
            chat_name=chat_name,
            type_=award_type,
            from_user=from_user,
            to_user=to_user,
            message=message,
        )
