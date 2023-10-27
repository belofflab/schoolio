from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from data.config import CHANNEL_ID, CHANNEL_URL
from loader import bot


class IsChatMember(BoundFilter):
    async def check(_, callback: CallbackQuery):
        member = await bot.get_chat_member(
            chat_id=CHANNEL_ID, user_id=callback.from_user.id
        )
        
        if not member.status == "left":
            return True
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f"""
Чтобы использоваться бот, для начала подпишитесь на <a href="{CHANNEL_URL}">наш канал!</a>

Жмите /start для повторной проверки
""",
        )
        return False
