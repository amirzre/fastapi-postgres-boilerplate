from uuid import UUID

from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController
from core.exceptions import NotFoundException


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
