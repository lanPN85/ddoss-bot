from telegram.ext import filters, ContextTypes, MessageHandler
from injectable import injectable, autowired, Autowired
from telegram import Update, MessageEntity
from loguru import logger
from src.handlers.awards import AwardCommandHandler


@injectable(singleton=True)
class HelpCommandHandler(MessageHandler):
    """Responds to help command"""

    COMMAND_PREFIX = "/help"

    @autowired
    def __init__(self, award_handler: Autowired(AwardCommandHandler)):
        super().__init__(filters=filters.ALL, callback=self.callback)
        self.award_handler: AwardCommandHandler = award_handler

    async def callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message is None:
            return
        if update.message.text is None:
            return
        if not update.message.text.startswith("/help"):
            return

        await update.message.reply_text(
            "__Tặng phiếu bé ngoan__\n"
            f"```\n{self.award_handler.upvote_template_string}\n```\n"
            "__Tặng phiếu bé hư__\n"
            f"```\n{self.award_handler.downvote_template_string}\n```\n"
            "\n"
            f"Mỗi người được phép tặng tối đa {self.award_handler.award_limit or 'vô hạn'} phiếu mỗi ngày",
            parse_mode="Markdown",
        )
