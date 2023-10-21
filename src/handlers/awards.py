from telegram.ext import filters, ContextTypes, MessageHandler
from injectable import injectable, autowired, Autowired
from telegram import Update, MessageEntity
from asyncio import Lock
from loguru import logger
from datetime import date
from strenum import StrEnum

from src.db.base import IDatabaseHelper
from src.model import Award, AwardType


class CommandParseError(StrEnum):
    INVALID = "invalid"
    NO_INTENT = "no_intent"
    NO_TARGET = "no_target"


class AwardCommandHandler(MessageHandler):
    """Responds to award command"""

    UPVOTE_STICKER_ID = (
        "CAACAgUAAx0CfkbxYQADXWUzr797w2UVRRGCIQ9oCT0kXrbBAALZCQACO5tgVshOxj70tmM4MAQ"
    )
    DOWNVOTE_STICKER_ID = (
        "CAACAgUAAx0CfkbxYQADS2Uzcdq_YGE4TRtTbhAktnHVGD0RAALrBwACRin5VHjhGcim1L5hMAQ"
    )
    UPVOTE_PREFIX = "/up"
    DOWNVOTE_PREFIX = "/down"

    @autowired
    def __init__(
        self,
        bot_name: str,
        award_limit: int | None,
        db_helper: Autowired(IDatabaseHelper),
    ):
        super().__init__(filters=filters.ALL, callback=self.callback)
        self.bot_name = bot_name
        self.award_limit = award_limit
        self.db_helper: IDatabaseHelper = db_helper
        self.write_lock = Lock()

    @property
    def upvote_template_string(self) -> str:
        return f"{self.UPVOTE_PREFIX} <thông điệp + mention người nhận phiếu>"

    @property
    def downvote_template_string(self) -> str:
        return f"{self.DOWNVOTE_PREFIX} <thông điệp + mention người nhận phiếu>"

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        award = self._parse_update(update)

        if isinstance(award, CommandParseError):
            if award == CommandParseError.NO_TARGET:
                await update.message.reply_text(
                    "Mention người được nhận đi bác. Không thì tặng phiếu cho ai 🫣"
                )

            return

        if award.to_user == award.from_user:
            await update.message.reply_text("Tự cho mình phiếu bé ngoan?? Cút.")
            return

        async with self.write_lock:
            if self.award_limit is not None:
                current_award_count = await self.db_helper.count_user_awards_today(
                    award.from_user
                )

                if current_award_count >= self.award_limit:
                    await update.message.reply_text(
                        f"Một ngày chỉ được cho {self.award_limit} phiếu thôi. Okay?"
                    )
                    return

            await self.db_helper.insert_award(award)

        await update.message.reply_text(
            f"Ghi nhận phiếu {'bé ngoan' if award.type_ == AwardType.UPVOTE else 'bé hư'} từ {award.from_user} đến {award.to_user}",
        )

        sticker_id = (
            self.UPVOTE_STICKER_ID
            if award.type_ == AwardType.UPVOTE
            else self.DOWNVOTE_STICKER_ID
        )

        await update.message.reply_sticker(
            sticker=sticker_id,
        )

    def _parse_update(self, update: Update) -> Award | CommandParseError:
        if update.message is None:
            return CommandParseError.INVALID
        if update.message.text is None:
            return CommandParseError.INVALID
        if not update.message.text.startswith(self.UPVOTE_PREFIX) and not update.message.text.startswith(self.DOWNVOTE_PREFIX):
            return CommandParseError.NO_INTENT

        # Get name of the source user
        from_user = update.message.from_user.name
        chat_name = update.message.chat.title

        # Get award type
        award_type = None
        prefix = ""
        if update.message.text.startswith(f"{self.UPVOTE_PREFIX}"):
            award_type = AwardType.UPVOTE
            prefix = self.UPVOTE_PREFIX
        elif update.message.text.startswith(f"{self.DOWNVOTE_PREFIX}"):
            award_type = AwardType.DOWNVOTE
            prefix = self.DOWNVOTE_PREFIX

        mentions = update.message.parse_entities(types=[MessageEntity.TEXT_MENTION, MessageEntity.MENTION])

        # Find to_user
        to_user: str | None = None

        # to_user = "lanpn"

        for entity, text in mentions.items():
            if entity.user is None:
                to_user = str(text)
            else:
                to_user = entity.user.name

        if to_user is None:
            return CommandParseError.NO_TARGET

        # Find the award message
        message = ""
        command_offset = update.message.text.find(prefix)
        if command_offset != -1:
            message = update.message.text[
                command_offset + len(prefix) + 1 :
            ]

        return Award(
            chat_name=chat_name,
            type_=award_type,
            from_user=from_user,
            to_user=to_user,
            message=message,
        )
