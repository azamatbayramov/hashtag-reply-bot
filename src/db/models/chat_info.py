from beanie import Document
from pydantic import BaseModel


class HashTagReplyInfo(BaseModel):
    hash_tag: str
    reply_message: str


class ChatInfo(Document):
    chat_id: int
    hash_tags: list[HashTagReplyInfo]
