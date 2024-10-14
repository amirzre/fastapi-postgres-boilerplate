from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.controllers import UserController
from app.schemas.request import RegisterUserRequest
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


@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(
    register_user_request: RegisterUserRequest,
    user_controller: UserController = Depends(Factory().get_user_controller),
) -> UserResponse:
    """
    Register new user.
    """
    return await user_controller.register_user(register_user_request=register_user_request)
