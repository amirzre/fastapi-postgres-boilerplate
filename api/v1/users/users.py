from uuid import UUID

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


@user_router.get("/{id}")
async def get_user(id=UUID, user_controller: UserController = Depends(Factory().get_user_controller)) -> UserResponse:
    """
    Retrieve user by ID.
    """
    return await user_controller.get_user(user_uuid=id)
