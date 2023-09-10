from src.middleware.auth import JWTBearer

from src.utils import tokenizator


class AdminBearer(JWTBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error)

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid = super().verify_jwt(jwtoken)
        if is_token_valid:
            payload = tokenizator.decode(jwtoken)
            is_admin = payload.get("is_admin")
            if is_admin is not None:
                if is_admin:
                    return True
        return False
