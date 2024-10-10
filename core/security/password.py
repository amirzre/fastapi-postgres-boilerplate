from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt


class PasswordHandler:
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    @staticmethod
    def hash(password: str) -> str:
        return PasswordHandler.pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        normalized_hash = bcrypt.normhash(hashed_password)
        return PasswordHandler.pwd_context.verify(plain_password, normalized_hash)
