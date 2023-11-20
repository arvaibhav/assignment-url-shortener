from fastapi import APIRouter

from .auth.router import router as auth_router
from .user.router import router as user_router
from .url_shortener.router import router as url_shortener_router
from .url_shortener.router import redirection_router

base_router = APIRouter()
base_router.include_router(router=redirection_router, tags=["fetch_base_url"])
base_router.include_router(router=auth_router, prefix="/auth", tags=["auth"])
base_router.include_router(router=user_router, prefix="/user", tags=["user"])
base_router.include_router(
    router=url_shortener_router, prefix="/url_shortener", tags=["url_shortener"]
)
