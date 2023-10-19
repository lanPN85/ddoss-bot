from abc import ABC, abstractmethod
from src.model import MessageKey, MessageType


class IDatabaseHelper(ABC):
    @abstractmethod
    async def increment_message_count(self, key: MessageKey):
        raise NotImplementedError
