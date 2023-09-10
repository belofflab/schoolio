from typing import Union

import aiohttp
from aiogram import types
from data.config import DOMAIN
from keyboards.user import inline as inline_keyboard
from loader import api_client, dp
from decimal import Decimal


async def fetch_photo_data(photo_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None


@dp.message_handler(commands="start")
async def start(
    message: Union[types.Message, types.CallbackQuery], course="None", **kwargs
) -> None:
    api_client.make_request(
        "POST",
        endpoint="users/", user_id=message.from_user.id,
        data={"idx": message.from_user.id, "username": message.from_user.username},
    )
    if isinstance(message, types.Message):
        await message.answer_photo(
            photo=await fetch_photo_data("https://" + DOMAIN + "/media/banner.png"),
            caption="Доступные курсы: ",
            reply_markup=inline_keyboard.show_courses(user_id=message.from_user.id),
        )
    elif isinstance(message, types.CallbackQuery):
        message: types.CallbackQuery
        new_media = types.InputMediaPhoto(
            media="https://" + DOMAIN + "/media/banner.png", caption="Доступные курсы: "
        )
        await message.message.edit_media(
            media=new_media, reply_markup=inline_keyboard.show_courses(user_id=message.from_user.id)
        )


async def list_lessons(callback: types.CallbackQuery, course, **kwargs):
    status, course_detail = api_client.make_request(
        method="GET", endpoint=f"courses/{course}/", user_id=callback.from_user.id
    )
    if not status: return await callback.answer("Курс не найден")
    price = Decimal(course_detail.get("price"))
    price_15 = (price / 100) * 15

    new_media = types.InputMediaPhoto(
        media=f"https://{DOMAIN}/{course_detail.get('preview')}",
        caption=f"""
Курс: <b>{course_detail.get("title")}</b>

<b>{course_detail.get("description")}</b>

Цена: <s>{price + price_15}</s> {course_detail.get("price")}₽
""",
    )
    await callback.message.edit_media(
        media=new_media, reply_markup=inline_keyboard.show_lessons(course=course, user_id=callback.from_user.id)
    )


async def show_lesson(callback: types.CallbackQuery, course, lesson):
    status, lesson_detail = api_client.make_request(
        method="GET",
        endpoint=f"courses/{course}/lesson_blocks/{lesson}/",
        user_id=callback.from_user.id
    )
    if not status: return await callback.answer("Уроки не найдены")
    new_media = types.InputMediaPhoto(
        media=f"https://{DOMAIN}/{lesson_detail.get('preview')}",
        caption=f"""
В этом блоке: <b>{lesson_detail.get("title")}</b>

<b>{lesson_detail.get("description")}</b>
""",
    )
    await callback.message.edit_media(
        media=new_media,
        reply_markup=inline_keyboard.show_lesson(
            course=course, lesson=lesson, user_id=callback.from_user.id
        ),
    )


@dp.callback_query_handler(inline_keyboard.courses_cd.filter())
async def courses_navigate(callback: types.CallbackQuery, callback_data: dict):
    level = callback_data.get("level")
    course = callback_data.get("course")
    lesson = callback_data.get("lesson")

    levels = {"0": start, "1": list_lessons, "2": show_lesson}

    current_level_function = levels[level]

    await current_level_function(callback, course=course, lesson=lesson)
