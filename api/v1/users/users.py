from fastapi import APIRouter, Depends

from app.controllers import UserController
from app.schemas.response import UserResponse
from core.factory import Factory

user_router = APIRouter()


@user_router.get("/")
async def get_users(user_controller: UserController = Depends(Factory().get_user_controller)) -> list[UserResponse]:
    """
    Retrieve users.
    """
    return await user_controller.get_all()
