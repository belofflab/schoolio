from uuid import UUID

import ormar.exceptions
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.data.config import ALLOWED_ORIGINS
from src.database import models
from src.database.connection import database
from src.routers import courses, info, users
from src.utils import tokenizator

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/media", StaticFiles(directory="media"), name="media")


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


@app.get("/api/v1/courses/{course}/lesson_blocks/{lesson_block}/show")
async def show_lesson_block(
    request: Request, course: int, lesson: int, access: str
):
    # TODO: Make user access to video (Add security)
    is_auth = tokenizator.check(access)
    if not is_auth:
        return HTTPException(status_code=403, detail="Невалидный токен")
    s_course = await models.Course.objects.prefetch_related("lesson_blocks").get_or_none(
        idx=course
    )
    if not s_course:
        raise HTTPException(
            status_code=404, detail="Данный курс не был найден"
        )
    lesson_block = next(
        (block for block in s_course.lesson_blocks if block.order == lesson), None
    )
    if not lesson_block:
        raise HTTPException(
            status_code=404,
            detail=f"Учебный блок курса «{s_course.title}» не был найден",
        )
    return templates.TemplateResponse(
        "video.html",
        {"request": request, "lesson": lesson, "course": course, "access": access, "lesson_block": lesson_block},
    )


app.include_router(info.router)
app.include_router(users.router)
app.include_router(courses.router)
