from .base import IDatabaseHelper
from src.model import MessageKey, MessageType


class PostgresDatabaseHelper(IDatabaseHelper):
    def __init__(self) -> None:
        super().__init__()

    async def increment_message_count(self, key: MessageKey):
        return await super().increment_message_count(key)
