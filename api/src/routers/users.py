import typing as t
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from src.database import models
from src.schemas import (
    User,
    UserCreate,
    UserOTPVerify,
    UserPaymentRequest,
    UserPaymentRequestCreate,
    UserPaymentRequestPatch,
)
from src.utils import hashing, telegram_bot, tokenizator, files

router = APIRouter(prefix="/api/v1/users", tags=["Пользователи"])


@router.post("/")
async def get_or_create_user(user: UserCreate) -> User:
    s_user = await models.User.objects.get_or_none(idx=user.idx)

    if s_user:
        if s_user.username != user.username:
            await s_user.update(username=user.username)
    else:
        s_user = await models.User.objects.create(**user.dict())

    return s_user


@router.post("/access/{user_idx}/")
async def create_access(user_idx: int):
    user = await models.User.objects.get_or_none(idx=user_idx)

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # if tokenizator.check(user.last_jwt_token):
    #     raise HTTPException(
    #         status_code=403,
    #         detail=str(user.last_jwt_token),
    #     )
    new_token = tokenizator.create(
        user_id=user.idx, is_admin=user.is_admin, is_active=user.is_active
    )
    await user.update(last_jwt_token=new_token)
    return {"token": new_token}


@router.post("/signin")
async def signin(user: UserCreate):
    q_user = await models.User.objects.get_or_none(idx=user.idx)

    if q_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверная почта или пароль"
        )

    if q_user is not None and not q_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Сначала вам нужно зарегистровать аккаунт с ID: {user.idx}",
        )

    if not hashing.Hasher.verify_password(user.password, q_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверная почта или пароль"
        )

    access_token = tokenizator.create(
        user_id=q_user.idx, is_admin=q_user.is_admin, is_active=q_user.is_active
    )

    q_user.password = ""
    q_user = q_user.dict()
    q_user.update({"access_token": access_token})

    return q_user


@router.post("/signup")
async def signup(user: UserCreate) -> User:
    q_user = await models.User.objects.get_or_none(idx=user.idx)
    if q_user is not None:
        if q_user.password is not None and q_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь уже существует",
            )

        await q_user.generate_otp_secret()
        is_deliveried = await telegram_bot.send_message(
            user.idx, text=f"Ваш проверочный код: <code>{q_user.otp_secret}</code>"
        )
        if not is_deliveried:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пожалуйста, разблокируйте бота",
            )
    else:
        user.password = hashing.Hasher.get_password_hash(user.password)

        new_player = await models.User.objects.create(**user.dict())
        await new_player.generate_otp_secret()
        is_deliveried = await telegram_bot.send_message(
            user.idx, text=f"Ваш проверочный код: <code>{new_player.otp_secret}</code>"
        )
        if not is_deliveried:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пожалуйста, разблокируйте бота",
            )

    raise HTTPException(status_code=status.HTTP_200_OK)


@router.post("/verify")
async def verify_registration(data: UserOTPVerify):
    user = await models.User.objects.get_or_none(idx=data.idx)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    if not await user.validate_otp(data.otp):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильный OTP"
        )

    if user.password is None and data.password is not None:
        user.password = hashing.Hasher.get_password_hash(data.password)

    user.is_active = True

    await user.update()

    access_token = tokenizator.create(
        user_id=user.idx, is_admin=user.is_admin, is_active=user.is_active
    )
    user.password = ""
    user = user.dict()
    user.update({"access_token": access_token})

    return user


@router.get("/me")
async def me(token: str):
    isTokenValid: bool = False

    try:
        payload = tokenizator.decode(token)
    except:
        payload = None
    if payload:
        isTokenValid = True

    if not isTokenValid:
        raise HTTPException(status_code=403, detail="Вы не авторизованы!")

    current_player = await models.User.objects.get(idx=payload["user_id"])
    current_player.password = ""
    return current_player


@router.post("/payment/requests/")
async def create_payment_request(
    payment_request: UserPaymentRequestCreate = Depends(),
    receipt: t.Optional[UploadFile] = File(default=None),
) -> UserPaymentRequest:
    user = await models.User.objects.get_or_none(idx=payment_request.user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Работник не найден"
        )
    course = await models.Course.objects.get_or_none(idx=payment_request.course)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Курс не найден"
        )
    receipt_path = None
    if receipt:
        receipt_path = files.create(file=receipt, upath="receipts")

    return await models.UserPaymentRequest.objects.create(
        user=user, course=course, receipt=receipt_path
    )


@router.patch("/payment/requests/{idx}")
async def update_payment_request(
    idx: int,
    payment_request: UserPaymentRequestPatch,
) -> UserPaymentRequest:
    s_payment_request = await models.UserPaymentRequest.objects.prefetch_related(
        "course"
    ).get_or_none(idx=idx)
    if not s_payment_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Заявка не найдена"
        )
    await models.UserCourse.objects.create(
        user=s_payment_request.user, course=s_payment_request.course
    )

    return await s_payment_request.update(is_success=payment_request.is_success)
