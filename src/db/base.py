from abc import ABC, abstractmethod
from src.model import MessageKey, Award


class IDatabaseHelper(ABC):
    @abstractmethod
    async def increment_message_count(self, key: MessageKey):
        raise NotImplementedError

    @abstractmethod
    async def insert_award(self, award: Award) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_user_awards_today(self, user_name: str) -> int:
        raise NotImplementedError
