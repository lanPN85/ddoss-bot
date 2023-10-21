from strenum import StrEnum
from dataclasses import dataclass, field
from datetime import date, datetime


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


class AwardType(StrEnum):
    UPVOTE = "upvote"
    DOWNVOTE = "downvote"


@dataclass
class Award:
    chat_name: str
    type_: AwardType
    from_user: str
    to_user: str
    message: str
    awarded_at: datetime = field(default_factory=datetime.now)
