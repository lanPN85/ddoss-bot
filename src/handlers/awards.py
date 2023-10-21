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
    MISSING_VOTE_TYPE = "missing_vote_type"
    NO_TARGET = "no_target"
    HELP = "help"


class AwardCommandHandler(MessageHandler):
    """Responds to award command"""

    UPVOTE_STICKER_ID = (
        "CAACAgUAAx0CfkbxYQADXWUzr797w2UVRRGCIQ9oCT0kXrbBAALZCQACO5tgVshOxj70tmM4MAQ"
    )
    DOWNVOTE_STICKER_ID = (
        "CAACAgUAAx0CfkbxYQADS2Uzcdq_YGE4TRtTbhAktnHVGD0RAALrBwACRin5VHjhGcim1L5hMAQ"
    )
    COMMAND_PREFIX = "/give"

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
    def template_string(self) -> str:
        return f"{self.COMMAND_PREFIX} +1/-1 <thông điệp + mention người nhận phiếu>"

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        award = self._parse_update(update)

        if isinstance(award, CommandParseError):
            if award == CommandParseError.MISSING_VOTE_TYPE:
                await update.message.reply_text(
                    f"Sai cú pháp 🤮🤮\n```\n{self.template_string}\n```",
                    parse_mode="Markdown",
                )
            if award == CommandParseError.NO_TARGET:
                await update.message.reply_text(
                    "Mention người được nhận đi bác. Không thì tặng phiếu cho ai 🫣"
                )
            if award == CommandParseError.HELP:
                await update.message.reply_text(
                    "Tặng phiếu bé ngoan/bé hư cho người khác bằng cách nhắn tin với cú pháp\n"
                    f"```\n{self.template_string}\n```\n"
                    "+1 ứng với phiếu bé ngoan. -1 ứng với phiếu bé hư\n"
                    f"VD: `{self.COMMAND_PREFIX} +1 Cảm ơn @user đã hỗ trợ trong công việc`\n"
                    f"Mỗi người được phép tặng tối đa {self.award_limit or 'vô hạn'} phiếu mỗi ngày",
                    parse_mode="Markdown",
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
            f"Ghi nhận phiếu {'bé ngoan' if award.type_ == AwardType.UPVOTE else 'bé hư'} từ {award.from_user} đến {award.to_user}\n```\n{award.message}\n```",
            parse_mode="Markdown",
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
        if not update.message.text.startswith(self.COMMAND_PREFIX):
            return CommandParseError.NO_INTENT
        if update.message.text.strip() == f"{self.COMMAND_PREFIX} help":
            return CommandParseError.HELP

        # Get name of the source user
        from_user = update.message.from_user.name
        chat_name = update.message.chat.title

        # Get award type
        award_type = None
        if update.message.text.startswith(f"{self.COMMAND_PREFIX} +1"):
            award_type = AwardType.UPVOTE
        elif update.message.text.startswith(f"{self.COMMAND_PREFIX} -1"):
            award_type = AwardType.DOWNVOTE
        else:
            return CommandParseError.MISSING_VOTE_TYPE

        mentions = update.message.parse_entities(types=[MessageEntity.TEXT_MENTION])

        # Find to_user
        to_user: str | None = None

        # to_user = "lanpn"

        for entity, text in mentions.items():
            if entity.user is None:
                continue
            to_user = entity.user.name

        if to_user is None:
            return CommandParseError.NO_TARGET

        # Find the award message
        message = ""
        command_offset = update.message.text.find(self.COMMAND_PREFIX)
        if command_offset != -1:
            message = update.message.text[
                command_offset + len(self.COMMAND_PREFIX) + 1 :
            ]

        return Award(
            chat_name=chat_name,
            type_=award_type,
            from_user=from_user,
            to_user=to_user,
            message=message,
        )
