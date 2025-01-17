from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

import config
from db.models.chat_info import ChatInfo

MODELS = [
    ChatInfo
]


async def init_db():
    client = AsyncIOMotorClient(config.MONGO_URI)
    await init_beanie(database=client.HashTagReplyBot, document_models=MODELS)
