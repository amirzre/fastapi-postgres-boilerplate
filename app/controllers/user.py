from uuid import UUID

from app.models import User, UserRole
from app.repositories import UserRepository
from core.controller import BaseController
from core.db import Transactional
from core.exceptions import BadRequestException, NotFoundException
from core.security import PasswordHandler


class UserController(BaseController[User]):
    """
    User controller provides all the logic operations for the User model.
    """

    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def get_user(self, *, user_uuid: UUID) -> User:
        user = await self.user_repository.get_by_uuid(uuid=user_uuid)
        if not user:
            raise NotFoundException(message="User not found.")
        return user

    @Transactional()
    async def register_user(
        self,
        *,
        email: str,
        password: str,
        first_name: str | None,
        last_name: str | None,
        role: UserRole | None,
        activated: bool | None,
    ) -> User:
        user = await self.user_repository.get_by_email(email=email)
        if user:
            raise BadRequestException(message="User already exists with this email.")

        password = PasswordHandler.hash(password=password)

        return await self.user_repository.create(
            {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "role": role,
                "activated": activated,
                "password": password,
            }
        )
