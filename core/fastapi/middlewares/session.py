from secrets import token_hex

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from core.config import config


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        session_id = request.cookies.get("Session-Id")
        if not session_id:
            session_id = token_hex(16)

        response = await call_next(request)
        response.set_cookie(
            key="Session-Id", value=session_id, httponly=True, samesite=True, max_age=config.SESSION_EXPIRE_MINUTES
        )
        return response
