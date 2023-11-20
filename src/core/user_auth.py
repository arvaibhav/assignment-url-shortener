from src.config import APP_CONFIG
from src.db.models import UserAuth
from src import schema
from src.utils.jwt_auth import create_jwt_token, fetch_jwt_token


async def create_jwt_token_for_user_auth(
    user_auth: UserAuth
) -> schema.UserJWTAuthToken:
    access_token_payload = schema.AccessTokenPayload(user_id=user_auth.user_id)
    token_id = user_auth.token_id
    access_token_payload.token_id = token_id

    # Create JWT token with the `auth_payload`
    access_token = create_jwt_token(
        data=access_token_payload.model_dump(),
        expires_in=user_auth.expires_in_sec,
    )

    # Create JWT Refresh Token with reference of last access id
    refresh_token = create_jwt_token(
        data=schema.RefreshTokenPayload(
            token_id=token_id, user_id=user_auth.user_id
        ).model_dump(),
        expires_in=APP_CONFIG.jwt_config.refresh_token_expires_in,
    )

    # Return the typical JWT view
    return schema.UserJWTAuthToken(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in_sec=user_auth.expires_in_sec,
        refresh_expires_in=APP_CONFIG.jwt_config.refresh_token_expires_in,
        user_id=user_auth.user_id,
    )


def get_access_token_payload(access_token) -> schema.AccessTokenPayload:
    """
    Raises:
        jwt.ExpiredSignatureError:
        jwt.DecodeError:
        jwt.PyJWTError: otherwise
    """
    payload: dict = fetch_jwt_token(token=access_token)
    return schema.AccessTokenPayload(**payload)


def get_refresh_token_payload(refresh_token) -> schema.RefreshTokenPayload:
    """
    Raises:
        jwt.ExpiredSignatureError:
        jwt.DecodeError:
        jwt.PyJWTError: otherwise
    """
    payload: dict = fetch_jwt_token(token=refresh_token)
    return schema.RefreshTokenPayload(**payload)
