from aiogram import types
from keyboards.user import inline as inline_keyboard
from filters.is_chat_member import IsChatMember
from loader import api_client, dp, bot
from data.config import API_URL, BASE_DIR, CHANNEL_ID, DOMAIN
from decimal import Decimal
import uuid
import requests
import os
from aiogram.dispatcher import FSMContext
from states.buy_course import BuyCourse
from keyboards.user import inline
from .menu import start, fetch_photo_data


async def list_courses(callback: types.CallbackQuery, **kwargs):
    await callback.message.edit_caption(
        caption="Доступные курсы: ",
        reply_markup=inline.show_courses(user_id=callback.from_user.id),
    )


async def proceed_buy_course(callback: types.CallbackQuery, course: str, detail: dict):
    detail = detail.get("detail").split("#")
    description = detail[0]
    price = detail[-1]
    await callback.message.edit_caption(
        f"<b>{description}</b>\n\nДля того, чтобы получить доступ к курсу нужно его приобрести",
        reply_markup=inline_keyboard.buy_lesson(course=course, price=price),
    )


@dp.callback_query_handler(lambda c: c.data.startswith("buy_course"))
async def buy_course(callback: types.CallbackQuery):
    course = callback.data.split("#")[1]
    price = callback.data.split("#")[2]
    await callback.message.edit_caption(
        f"""
<b>Вам выставлен счёт на оплату курса</b>

<b>Номер карты:</b> <code>2200 2460 9257 8163</code>
<b>Получатель:</b> Белов К.A
<b>Сумма:</b> <code>{price}</code>₽

P.S. Переводите только указанную сумму...
""",
        reply_markup=inline_keyboard.confirm_payment(course=course),
    )


@dp.callback_query_handler(
    lambda c: c.data == "decline_payment_request", state=BuyCourse.receipt
)
async def decline_payment_request(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await list_courses(callback=callback)


@dp.callback_query_handler(lambda c: c.data.startswith("confirm_payment"))
async def confirm_payment(callback: types.CallbackQuery, state: FSMContext):
    course = callback.data.split("#")[-1]
    new_message = await callback.message.edit_caption(
        "Отправьте сюда чек транзакции в формате <b>скриншота</b>",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="Отменить", callback_data="decline_payment_request"
            )
        ),
    )
    await BuyCourse.receipt.set()
    await state.set_data({"last_message_id": new_message.message_id, "course": course})


@dp.message_handler(
    content_types=[types.ContentType.PHOTO],
    state=BuyCourse.receipt,
)
async def control_user_payment_receipt(
    message: types.Message, state: FSMContext
) -> None:
    photo = message.photo
    cdata = await state.get_data()

    file_info = await bot.get_file(photo[-1].file_id)
    file_extension = file_info.file_path.split(".")[-1]
    unique_filename = str(uuid.uuid4()) + "." + file_extension
    output_file = BASE_DIR / f"media/{unique_filename}"
    await photo[-1].download(destination_file=output_file)
    params = {"user": message.from_user.id, "course": cdata.get("course")}
    with open(output_file, "rb") as file:
        new_lead_response = requests.post(
            API_URL + f"users/payment/requests/", params=params, files={"receipt": file}
        )
    new_lead_data = new_lead_response.json()

    await message.delete()
    await state.finish()
    new_message = await bot.edit_message_caption(
        chat_id=message.from_user.id,
        caption="Вы успешно отправили чек!\n\n<b>Ожидайте подтверждения оплаты...</b>",
        reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton(
                text="В главное меню",
                callback_data=inline_keyboard.make_courses_cd(level=0),
            )
        ),
        message_id=cdata.get("last_message_id"),
    )
    await bot.send_photo(
        chat_id=CHANNEL_ID,
        caption=f"<b>Новая заявка на пополнение</b>\n\nКурс: {new_lead_data.get('course').get('title')}\nСумма: {new_lead_data.get('course').get('price')}₽",
        photo=types.InputFile(output_file),
        reply_markup=inline.confirm_deposit_request_keyboard(
            new_lead_data.get("idx"), message.from_user.id, new_message.message_id
        ),
    )

    os.remove(output_file)


@dp.callback_query_handler(lambda c: c.data.startswith("patch_payment_request"))
async def deposit_request_confirm(callback: types.CallbackQuery):
    splitted_data = callback.data.split("#")
    move = splitted_data[1]
    request_id = int(splitted_data[2])
    user_id = int(splitted_data[3])
    last_message_id = int(splitted_data[4])
    response_data = None
    if move == "confirm":
        response = requests.patch(
            API_URL + f"users/payment/requests/{request_id}/",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json={
                "is_success": True,
            },
        )
        response_data = response.json()
    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n{'✅ Одобрена' if move == 'confirm' else '❌ Отклонена'}"
    )

    await bot.edit_message_caption(
        # media=types.InputMediaPhoto(
        #     media=await fetch_photo_data(
        #         f'https://{DOMAIN}/{response_data.get("course").get("preview")}'
        #         if move == "confirm"
        #         else f"https://{DOMAIN}/media/banner.png"
        #     ),
            # caption=f"Ваша заявку на покупку курса <b>{response_data}</b> одобрена!"
            # if move == "confirm"
            # else f"Ваша заявку на покупку курса отклонена",
        # ),
        caption=f"Ваша заявку на покупку курса <b>{response_data.get('course').get('title')}</b> одобрена!"
            if move == "confirm"
            else f"<b>Ваша заявку на покупку курса отклонена</b>",
        chat_id=user_id,
        message_id=last_message_id,
        reply_markup=inline_keyboard.show_courses(user_id=user_id),
    )


async def list_lessons(callback: types.CallbackQuery, course, **kwargs):
    status, course_detail = api_client.make_request(
        method="GET", endpoint=f"courses/{course}/", user_id=callback.from_user.id
    )
    if not status:
        return await proceed_buy_course(
            callback=callback, course=course, detail=course_detail
        )
    new_media = types.InputMediaPhoto(
        media=f"https://{DOMAIN}/{course_detail.get('preview')}",
        caption=f"""
Курс: <b>{course_detail.get("title")}</b>

<b>{course_detail.get("description")}</b>

Цена: {course_detail.get("price")}₽
""",
    )
    await callback.message.edit_media(
        media=new_media,
        reply_markup=inline_keyboard.show_lessons(
            course=course, user_id=callback.from_user.id
        ),
    )


async def show_lesson(callback: types.CallbackQuery, course, lesson):
    status, lesson_detail = api_client.make_request(
        method="GET",
        endpoint=f"courses/{course}/lesson_blocks/{lesson}/",
        user_id=callback.from_user.id,
    )
    if not status:
        return await callback.answer("Уроки не найдены")
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


@dp.callback_query_handler(IsChatMember(), inline_keyboard.courses_cd.filter())
async def courses_navigate(callback: types.CallbackQuery, callback_data: dict):
    level = callback_data.get("level")
    course = callback_data.get("course")
    lesson = callback_data.get("lesson")

    levels = {"0": start, "1": list_courses, "2": list_lessons, "3": show_lesson}

    current_level_function = levels[level]

    await current_level_function(callback, course=course, lesson=lesson)
