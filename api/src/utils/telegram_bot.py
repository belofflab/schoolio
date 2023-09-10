from aiogram import Bot
# from aiogram.utils.exceptions import ChatNotFound
from src.data.config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")


async def send_message(chat_id: int, text: str) -> bool:
    is_deliveried = False
    try:
        await bot.send_message(chat_id=chat_id, text=text)
        is_deliveried = True
    except:
        pass

    return is_deliveried
