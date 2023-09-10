import time

import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError
from src.data.config import SECRET_KEY


def create(user_id: int, is_admin: bool, is_active: bool, expires_in: int = 30) -> str:
    return jwt.encode(
        payload={
            "user_id": user_id,
            "is_admin": is_admin,
            "is_active": is_active,
            "expires_in": time.time() + 60 * expires_in,
        },
        key=SECRET_KEY,
    )


def check(token: str) -> bool:
    result = False
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
        if payload["expires_in"] >= time.time():
            result = True
    except (InvalidSignatureError, DecodeError):
        return result

    return result


def decode(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token if decoded_token["expires_in"] >= time.time() else None
    except:
        return {}
