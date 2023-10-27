from typing import Union

import aiohttp
from aiogram import types
from data.config import DOMAIN
from keyboards.user import inline as inline_keyboard
from filters.is_chat_member import IsChatMember
from loader import api_client, dp


async def fetch_photo_data(photo_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None


WELCOME_MESSAGE = """
Добро пожаловать, {full_name}!

Тебя приветсвует наша <b>Лаборатория [name]</b>, где мы реализуем будущие таланты ;)
"""

FREE_MESSAGE = """
Получите начальный вектор прямо сейчас! 

<b>Начальный вектор</b> - точка, откуда нужно стартовать, чтобы стать квалифицированным специалистом в своей области. 

На консультации мы

✔️ Прорабатываем общую эрудицию и подбираем подходящую професиию
✔️ Решаем текущие задачи
✔️ Обучаем новым технологиям и подбираем личный <b>RoadMap</b>

👨‍🏫 @belofflab
"""


@dp.message_handler(commands="start")
async def start(
    message: Union[types.Message, types.CallbackQuery], course="None", **kwargs
) -> None:
    api_client.make_request(
        "POST",
        endpoint="users/",
        user_id=message.from_user.id,
        data={"idx": message.from_user.id, "username": message.from_user.username},
    )
    if isinstance(message, types.Message):
        await message.answer_photo(
            photo=await fetch_photo_data("https://" + DOMAIN + "/media/banner.png"),
            caption=WELCOME_MESSAGE.format(full_name=message.from_user.full_name),
            reply_markup=inline_keyboard.menu(),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        new_media = types.InputMediaPhoto(
            media="https://" + DOMAIN + "/media/banner.png",
            caption=WELCOME_MESSAGE.format(full_name=message.from_user.full_name),
        )
        await message.message.edit_media(
            media=new_media,
            reply_markup=inline_keyboard.menu(),
        )


@dp.callback_query_handler(lambda c: c.data == "free")
async def free(callback: types.CallbackQuery):
    await callback.message.edit_caption(
        caption=FREE_MESSAGE,
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Назад", callback_data=inline_keyboard.make_courses_cd(0)
            )
        ),
    )
