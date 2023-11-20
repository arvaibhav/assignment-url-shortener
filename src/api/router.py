from fastapi import APIRouter

# from .auth.router import router as auth_router
from .user.router import router as user_router

base_router = APIRouter()
# base_router.include_router(router=auth_router, prefix="/auth", tags=["auth"])
base_router.include_router(router=user_router, prefix="/user", tags=["user"])
