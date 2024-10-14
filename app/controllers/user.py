from uuid import UUID

from app.models import User, UserRole
from app.repositories import UserRepository
from app.schemas.request import RegisterUserRequest
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
    async def register_user(self, *, register_user_request: RegisterUserRequest) -> User:
        user = await self.user_repository.get_by_email(email=register_user_request.email)
        if user:
            raise BadRequestException(message="User already exists with this email.")

        hashed_password = PasswordHandler.hash(password=register_user_request.password)

        user_data = register_user_request.model_dump(exclude_unset=True)
        user_data["password"] = hashed_password
        return await self.user_repository.create(attributes=user_data)
