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
    type_: MessageType
    user_name: str
    chat_name: str
    topic_name: str
