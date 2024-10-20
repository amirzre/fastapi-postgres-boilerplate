import secrets

from pydantic import EmailStr
from redis.asyncio import client

from app.models import User
from app.repositories import UserRepository
from app.schemas.extra import Token
from app.schemas.request import UserLoginRequest
from core.controller import BaseController
from core.exceptions import BadRequestException
from core.security import JWTHandler, PasswordHandler


class AuthController(BaseController[User]):
    """
    Auth controller provides all the logic operations for the user authentication.
    """

    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def login(self, *, login_user_request: UserLoginRequest, cache: client.Redis) -> Token:
        user = await self.user_repository.get_by_email(email=login_user_request.email)
        if not user:
            raise BadRequestException(message="Invalid credentials.")
        if not PasswordHandler.verify(user.password, login_user_request.password):
            raise BadRequestException(message="Invalid credentials.")
        if user.activated is False:
            raise BadRequestException(message="The user is inactive.")

        refresh_token = JWTHandler.encode_refresh_token(
            payload={"sub": "refresh_token", "verify": str(user.uuid), "role": user.role}
        )
        access_token = JWTHandler.encode(payload={"uuid": str(user.uuid), "role": user.role})
        csrf_token = secrets.token_hex(32)

        await cache.set(name=refresh_token, value=str(user.uuid), ex=JWTHandler.refresh_token_expire)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            csrf_token=csrf_token,
        )
