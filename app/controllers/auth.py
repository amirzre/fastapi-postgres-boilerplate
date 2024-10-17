from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    ...
