from fastapi import APIRouter, HTTPException, status
from src.database import models
from src.schemas import User, UserCreate, UserOTPVerify
from src.utils import hashing, telegram_bot, tokenizator

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
        return HTTPException(status_code=404, detail="Пользователь не найден")

    if tokenizator.check(user.last_jwt_token):
        return HTTPException(
            status_code=403,
            detail=str(user.last_jwt_token),
        )
    new_token = tokenizator.create(
        user_id=user.idx, is_admin=user.is_admin, is_active=user.is_active
    )
    await user.update(last_jwt_token=new_token)
    return {"token": new_token}


@router.post("/signin")
async def signin(user: UserCreate):
    q_user = await models.User.objects.get_or_none(idx=user.idx)

    if q_user is None:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверная почта или пароль"
        )

    if q_user is not None and not q_user.is_active:
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Сначала вам нужно зарегистровать аккаунт с ID: {user.idx}",
        )

    # if not hashing.Hasher.verify_password(user.password, q_user.password):
    #     return HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail="Неверная почта или пароль"
    #     )

    access_token =  tokenizator.create(
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
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь уже существует",
            )

        await q_user.generate_otp_secret()
        is_deliveried = await telegram_bot.send_message(
            user.idx, text=f"Ваш проверочный код: <code>{q_user.otp_secret}</code>"
        )
        if not is_deliveried:
            return HTTPException(
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
            return HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пожалуйста, разблокируйте бота",
            )

    return HTTPException(status_code=status.HTTP_200_OK)


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

    access_token =  tokenizator.create(
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
        return HTTPException(status_code=403, detail="Вы не авторизованы!")

    current_player = await models.User.objects.get(idx=payload["user_id"])
    current_player.password = ""
    return current_player
