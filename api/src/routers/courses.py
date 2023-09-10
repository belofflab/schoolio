from typing import List, Union

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from ormar.exceptions import NoMatch
from src.database import models
from src.middleware import admin, auth
from src.schemas import Course, CourseCreate, LessonBlock, LessonBlockCreate
from src.utils import files, tokenizator

router = APIRouter(prefix="/api/v1/courses", tags=["Курсы"])


async def is_student_or_admin(request: Request, course: Course):
    jwt_token = request.headers.get("authorization").split(" ")[-1]
    payload = tokenizator.decode(jwt_token)
    user_id = payload.get("user_id")
    is_admin = payload.get("is_admin")

    is_user_course = await models.UserCourse.objects.get_or_none(
        user=user_id, course=course
    )
    if not is_user_course and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Этот курс ещё не приобретён"
        )


@router.get("/", dependencies=[Depends(auth.JWTBearer())])
async def get_courses() -> List[Course]:
    return await models.Course.objects.all()


@router.get("/{course}/", dependencies=[Depends(auth.JWTBearer())])
async def get_course(course: int, request: Request) -> Union[Course, HTTPException]:
    current_course = await models.Course.objects.get_or_none(idx=course)
    if not current_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Курс не был найден"
        )

    await is_student_or_admin(request=request, course=current_course)

    return current_course


@router.get("/{course}/lesson_blocks/", dependencies=[Depends(auth.JWTBearer())])
async def get_lesson_blocks(
    request: Request, course: int
) -> Union[List[LessonBlock], HTTPException]:
    try:
        current_course = (
            await models.Course.objects.filter(idx=course)
            .prefetch_related("lesson_blocks")
            .first()
        )
        current_course = current_course.lesson_blocks

        await is_student_or_admin(request=request, course=current_course)
    except NoMatch:
        current_course = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данный курс не был найден"
        )
    finally:
        return current_course


@router.get("/{course}/lesson_blocks/{lesson}/", dependencies=[Depends(auth.JWTBearer())])
async def get_lesson_block(
    request: Request, course: int, lesson: int
) -> Union[LessonBlock, HTTPException]:
    course_obj = await models.Course.objects.select_related(
        "lesson_blocks"
    ).get_or_none(idx=course)

    if not course_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Данный курс не был найден"
        )

    lesson_block = next(
        (block for block in course_obj.lesson_blocks if block.order == lesson), None
    )

    if not lesson_block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Учебный блок курса «{course_obj.title}» не был найден",
        )

    await is_student_or_admin(request=request, course=course)

    return lesson_block


@router.post("/", dependencies=[Depends(admin.AdminBearer())])
async def create_course(
    course: CourseCreate = Depends(), preview: UploadFile = File(...)
) -> Union[Course, HTTPException]:
    if preview.content_type.split("/")[0] != "image":
        return HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Некорректный формат обложки",
        )
    new_course = await models.Course.objects.create(**course.dict())

    preview_path = files.create(file=preview, upath="previews")
    await new_course.update(preview=preview_path)

    return new_course


@router.post("/{course}/lesson_block/", dependencies=[Depends(admin.AdminBearer())])
async def create_lesson_block(
    course: int,
    lesson_block: LessonBlockCreate = Depends(),
    video: UploadFile = File(...),
    preview: UploadFile = File(...),
) -> Union[LessonBlock, HTTPException]:
    current_course = await models.Course.objects.prefetch_related(
        "lesson_blocks"
    ).get_or_none(idx=course)
    if not current_course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Курс не был найден"
        )

    next_order = len(current_course.lesson_blocks) + 1

    new_lesson_block = await models.LessonBlock.objects.create(
        **lesson_block.dict(), order=next_order
    )

    video_path = files.create(file=video, upath="videos")
    preview_path = files.create(file=preview, upath="previews")

    await new_lesson_block.update(video_url=video_path, preview=preview_path)

    await current_course.lesson_blocks.add(new_lesson_block)

    return new_lesson_block


@router.get("/{course}/lesson_blocks/{lesson_block}/video/", dependencies=[Depends(auth.JWTBearer())])
async def get_lesson_block_video(request: Request, course: int, lesson_block: int):
    current_course = await models.Course.objects.select_related(
        "lesson_blocks"
    ).get_or_none(idx=course)
    if not current_course:
        raise HTTPException(status_code=404, detail="Курс не был найден")

    lesson_blocks = current_course.lesson_blocks

    current_lesson_block = next(
        (block for block in lesson_blocks if block.idx == lesson_block), None
    )

    if not current_lesson_block or not current_lesson_block.video_url:
        raise HTTPException(
            status_code=404, detail="Учебный блок или видео не были найдены"
        )
    
    await is_student_or_admin(request=request, course=current_course)

    video_path = current_lesson_block.video_url

    video_extension = video_path.split(".")[-1]
    media_type = f"video/{video_extension}"

    return StreamingResponse(files.stream(video_path), media_type=media_type)
