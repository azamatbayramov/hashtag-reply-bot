import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message

from config import BOT_TOKEN
from db.models.chat_info import ChatInfo
from db.settings import init_db

dp = Dispatcher()


@dp.message(Command('init'))
async def init_chat(message: Message) -> None:
    chat_info = await ChatInfo.find(ChatInfo.chat_id == message.chat.id).first_or_none()
    if chat_info:
        await message.reply("This chat already initialized")
        return

    await ChatInfo(chat_id=message.chat.id, hashtag_replies={}).insert()


@dp.message(Command('add_hashtag_reply'))
async def add_hashtag_reply(message: Message) -> None:
    chat_info = await ChatInfo.find(ChatInfo.chat_id == message.chat.id).first_or_none()
    if not chat_info:
        await message.reply("Please, initialize the chat first")
        return

    args = message.text.split(' ', 2)

    if len(args) != 3:
        await message.reply("Usage: /add_hashtag_reply <hashtag without #> <reply>")
        return

    chat_info.hashtag_replies[args[1]] = args[2]
    await chat_info.save()

    await message.reply("Hashtag reply added")


@dp.message(Command('remove_hashtag_reply'))
async def remove_hashtag_reply(message: Message) -> None:
    chat_info = await ChatInfo.find(ChatInfo.chat_id == message.chat.id).first_or_none()
    if not chat_info:
        await message.reply("Please, initialize the chat first")
        return

    args = message.text.split(' ', 1)

    if len(args) != 2:
        await message.reply("Usage: /remove_hashtag_reply <hashtag without #>")
        return

    if args[1] not in chat_info.hashtag_replies:
        await message.reply("Hashtag reply not found")
        return

    del chat_info.hashtag_replies[args[1]]
    await chat_info.save()

    await message.reply("Hashtag reply removed")


@dp.message(Command('list_hashtag_replies'))
async def list_hashtag_replies(message: Message) -> None:
    chat_info = await ChatInfo.find(ChatInfo.chat_id == message.chat.id).first_or_none()
    if not chat_info:
        await message.reply("Please, initialize the chat first")
        return

    if not chat_info.hashtag_replies:
        await message.reply("No hashtag replies")
        return

    reply = "Hashtag replies:\n"
    for hashtag, reply_text in chat_info.hashtag_replies.items():
        reply += f"#{hashtag}: {reply_text}\n"

    await message.reply(reply)


@dp.message()
async def hashtag_reply(message: Message) -> None:
    chat_info = await ChatInfo.find(ChatInfo.chat_id == message.chat.id).first_or_none()
    if not chat_info:
        return

    for hashtag in chat_info.hashtag_replies.keys():
        if f"#{hashtag}" in message.text:
            await message.reply(chat_info.hashtag_replies[hashtag])
            return


async def main() -> None:
    await init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='MarkdownV2'))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
