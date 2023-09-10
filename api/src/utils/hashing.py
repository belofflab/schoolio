from passlib.context import CryptContext
from passlib.exc import UnknownHashError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):
        try:
            result = pwd_context.verify(plain_password, hashed_password)
        except (UnknownHashError, ):
            result = None
        finally:
            return result

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)