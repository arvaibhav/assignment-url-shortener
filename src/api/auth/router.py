from fastapi import APIRouter, Body, HTTPException, Depends
from src.core.user_auth import get_refresh_token_payload, create_jwt_token_for_user_auth
from src.dao.auth import get_user_auth_by_id
from src.db.connection import get_db_client
from src.schema import UserJWTAuthToken

router = APIRouter()


@router.post("/token/refresh", response_model=UserJWTAuthToken)
async def validate_refresh_token(
    db_client=Depends(get_db_client), *, refresh_token=Body(..., embed=True)
):
    # Validate the refresh token
    try:
        refresh_token = get_refresh_token_payload(refresh_token)
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )

    user_auth = await get_user_auth_by_id(db_client, _id=refresh_token.token_id)
    if not user_auth.is_evoked:
        user_jwt_token = await create_jwt_token_for_user_auth(user_auth=user_auth)
        return user_jwt_token

    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token",
        )
