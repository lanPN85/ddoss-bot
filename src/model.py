from strenum import StrEnum
from dataclasses import dataclass
from datetime import date


class MessageType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


@dataclass
class MessageKey:
    date: date
    chat_id: int
    user_id: int
    type_: MessageType
    topic_name: str | None = None
