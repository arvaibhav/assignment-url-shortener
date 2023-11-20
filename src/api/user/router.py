from fastapi import APIRouter, HTTPException, Depends
from src import schema
from src.config import APP_CONFIG
from src.core.user_auth import create_jwt_token_for_user_auth
from src.dao.auth import create_user_auth
from src.dao.user import create_user, get_user_by_username
from src.db.connection import get_db_client
from src.db.models import UserAuth
from src.utils.string_hasher import hash_string, verify_hashed_string

router = APIRouter()


@router.post("/login", response_model=schema.UserProfile)
async def user_login(
    db_client=Depends(get_db_client),
    *,
    user_login_request: schema.UserAuthRequestSchema,
):
    user = await get_user_by_username(
        db_client=db_client, username=user_login_request.username
    )
    if not user:
        raise HTTPException(status_code=401, detail="username not found")
    if not verify_hashed_string(user_login_request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid password")

    user_auth: UserAuth = await create_user_auth(
        db_client=db_client,
        user_id=user.id,
        expires_in_sec=APP_CONFIG.jwt_config.token_expires_in,
    )
    user_jwt_token = await create_jwt_token_for_user_auth(user_auth=user_auth)
    return schema.UserProfile(
        auth_token=user_jwt_token,
        username=user.username,
        email=user.email,
        user_id=user.id,
    )


@router.post("/signup", response_model=schema.UserJWTAuthToken)
async def user_signup(
    db_client=Depends(get_db_client),
    *,
    user_signup_request: schema.UserSignupRequestSchema,
):
    if await get_user_by_username(
        db_client=db_client, username=user_signup_request.username
    ):
        raise HTTPException(
            status_code=401, detail="account with this username already created"
        )
    user = await create_user(
        db_client=db_client,
        username=user_signup_request.username,
        password_hash=hash_string(user_signup_request.password),
        email=user_signup_request.email,
    )
    user_auth: UserAuth = await create_user_auth(
        db_client=db_client,
        user_id=user.id,
        expires_in_sec=APP_CONFIG.jwt_config.token_expires_in,
    )
    user_jwt_token = await create_jwt_token_for_user_auth(user_auth=user_auth)
    return user_jwt_token
