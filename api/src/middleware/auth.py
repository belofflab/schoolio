from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils import tokenizator


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Неверная схема аутентификации.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="В доступе отказано. Проверьте права на пользование...")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Неверный код авторизации.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = tokenizator.decode(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid