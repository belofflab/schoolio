from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.callback_data import CallbackData
from loader import api_client
from uuid import UUID

from data.config import DOMAIN

courses_cd = CallbackData("courses", "level", "course", "lesson")


def make_courses_cd(level, course="-", lesson="-"):
    return courses_cd.new(level=level, course=course, lesson=lesson)


def show_courses(user_id: int):
    CURRENT_LEVEL = 0
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

    return markup


def show_lessons(course: int, user_id: int):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    status, response = api_client.make_request("GET", f"courses/{course}/lesson_blocks/", user_id=user_id)
    if status:
        lesson_blocks = sorted(response, key=lambda x: x['order'])

        for lesson_block in lesson_blocks:
            markup.row(
                InlineKeyboardButton(
                    text=f'Блок: {lesson_block.get("order")} ' + lesson_block.get("title"),
                    callback_data=make_courses_cd(
                        level=CURRENT_LEVEL + 1,
                        course=course,
                        lesson=lesson_block.get("idx"),
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

def show_lesson(course: int, lesson: str, user_id: int):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)
    status, response = api_client.make_request("POST", endpoint=f"users/access/{user_id}/", user_id=user_id)
    if status:
        if response.get("status_code") == 403:
            token = response.get("detail")
        else:
            token = response.get("token")

    markup.add(
        InlineKeyboardButton(
            "Посмотреть",
            web_app=WebAppInfo(url=f"""https://{DOMAIN}/api/v1/courses/{course}/lesson_blocks/{lesson}/show?access={token}""")
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

