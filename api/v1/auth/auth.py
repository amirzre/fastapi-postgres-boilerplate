from fastapi import APIRouter, Depends, Response, status
from redis.asyncio import client

from app.controllers import AuthController
from app.schemas.request import UserLoginRequest
from core.factory import Factory
from core.fastapi.dependencies import get_cache
from core.security import JWTHandler

auth_router = APIRouter()


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    login_user_request: UserLoginRequest,
    cache: client.Redis = Depends(get_cache),
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> None:
    """
    Login user.
    """
    tokens = await auth_controller.login(
        login_user_request=login_user_request,
        cache=cache,
    )

    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.access_token),
    )
    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
        expires=JWTHandler.token_expiration(tokens.refresh_token),
    )
    response.headers["X-CSRF-TOKEN"] = tokens.csrf_token
