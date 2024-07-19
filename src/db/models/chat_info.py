from beanie import Document


class ChatInfo(Document):
    chat_id: int
    hashtag_replies: dict[str, str]
