from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController


class UserController(BaseController[User]):
    """
    User controller provides all the logic operations for the User model.
    """

    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    ...
