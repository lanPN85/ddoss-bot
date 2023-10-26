from abc import ABC, abstractmethod
from telegram.ext import ExtBot


class IScheduledActor(ABC):
    @abstractmethod
    async def invoke(self, bot: ExtBot):
        raise NotImplementedError

    @abstractmethod
    def schedule(self) -> str | None:
        raise NotImplementedError
