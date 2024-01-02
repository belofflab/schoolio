from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.callback_data import CallbackData
from loader import api_client

from data.config import DOMAIN, CHANNEL_URL

courses_cd = CallbackData("courses", "level", "course", "lesson")
# buy_course_cd = CallbackData("buy_course", "level", "course", "")


def make_courses_cd(level, course="-", lesson="-"):
    return courses_cd.new(level=level, course=course, lesson=lesson)


def menu():
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        {"text": "🤜🤛 Бесплатная консультация", "callback_data": "free"},
        {
            "text": "🚀 Перейти к курсам",
            "callback_data": make_courses_cd(CURRENT_LEVEL + 1),
        },
        {
            "text": "👥 Чат общения",
            "url": CHANNEL_URL,
        },
        {
            "text": "🌐 Наш сайт",
            "url": "https://belofflab.com",
        },
        {
            "text": "📨 Связаться со мной",
            "url": "https://t.me/belofflab",
        },
    ]

    for button in buttons:
        markup.row(InlineKeyboardButton(**button))

    return markup


def show_courses(user_id: int):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    status, response = api_client.make_request("GET", "courses/", user_id=user_id)
    if status:
        for course in response:
            markup.row(
                InlineKeyboardButton(
                    text=course.get("title"),
                    callback_data=make_courses_cd(
                        level=CURRENT_LEVEL + 1, course=course.get("idx")
                    ),
                )
            )
    markup.row(
        InlineKeyboardButton(
            text="Назад", callback_data=make_courses_cd(CURRENT_LEVEL - 1)
        )
    )

    return markup


def show_lessons(course: int, user_id: int):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    status, response = api_client.make_request(
        "GET", f"courses/{course}/lesson_blocks/", user_id=user_id
    )
    if status:
        lesson_blocks = sorted(response, key=lambda x: x["order"])

        for lesson_block in lesson_blocks:
            markup.row(
                InlineKeyboardButton(
                    text=f'Блок: {lesson_block.get("order")} '
                    + lesson_block.get("title"),
                    callback_data=make_courses_cd(
                        level=CURRENT_LEVEL + 1,
                        course=course,
                        lesson=lesson_block.get("order"),
                    ),
                )
            )

    markup.add(
        InlineKeyboardButton(
            "Назад",
            callback_data=make_courses_cd(
                level=CURRENT_LEVEL - 1,
                course=course,
            ),
        )
    )

    return markup


def buy_lesson(course: int, price: str):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        {"text": "Оплатить", "callback_data": f"buy_course#{course}#{price}"},
        {
            "text": "Назад",
            "callback_data": make_courses_cd(
                level=CURRENT_LEVEL - 1,
                course=course,
            ),
        },
    ]
    for button in buttons:
        markup.insert(
            InlineKeyboardButton(**button)
        )

    return markup

def confirm_payment(course: str):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(
            text="Подтвердить",
            callback_data=f"confirm_payment#{course}"
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_courses_cd(level=1)
        )
    )

    return markup

def confirm_deposit_request_keyboard(request_id, user_id, last_message_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        {"text": "Подвердить ✅", "callback_data": f"patch_payment_request#confirm#{request_id}#{user_id}#{last_message_id}"},
        {"text": "Отклонить ❌", "callback_data": f"patch_payment_request#decline#{request_id}#{user_id}#{last_message_id}"},
    ]
    for button in buttons:
        markup.insert(InlineKeyboardButton(**button))

    return markup

def show_lesson(course: int, lesson: str, user_id: int):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup(row_width=1)
    status, response = api_client.make_request(
        "POST", endpoint=f"users/access/{user_id}/", user_id=user_id
    )
    if status:
        if response.get("status_code") == 403:
            token = response.get("detail")
        else:
            token = response.get("token")

    markup.add(
        InlineKeyboardButton(
            "Посмотреть",
            web_app=WebAppInfo(
                url=f"""https://{DOMAIN}/api/v1/courses/{course}/lesson_blocks/{lesson}/show?access={token}"""
            ),
        )
    )

    markup.add(
        InlineKeyboardButton(
            "Назад",
            callback_data=make_courses_cd(
                level=CURRENT_LEVEL - 1,
                course=course,
                lesson=lesson,
            ),
        )
    )

    return markup
