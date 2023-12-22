import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher

from config import API_TOKEN
from handlers import router
from db import db_start

storage = MemoryStorage()

operator = Bot(token=API_TOKEN,
               parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=storage)
dp.include_router(router)


async def setup_bot_commands():
    bot_commands = [
        BotCommand(command="/help", description="get info about bot"),
        BotCommand(command="/resize", description="to resize an image"),
        BotCommand(command="/rembg", description="to remove image background"),
        BotCommand(command="/lang", description="change locale"),
        BotCommand(command="/cancel", description="cancel current step"),
    ]
    await operator.set_my_commands(bot_commands)


async def on_startup():
    await setup_bot_commands()
    await db_start()


async def polling():
    await operator.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(operator,
                           allowed_updates=dp.resolve_used_update_types(),
                           on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.startup.register(on_startup)
    asyncio.run(polling())
