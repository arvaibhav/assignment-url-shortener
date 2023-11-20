from typing import Optional

from fastapi import Header

from src import schema
from src.core.user_auth import get_access_token_payload
from fastapi import HTTPException


def get_auth_token_payload(token: str = Header(alias="Authorization")) -> Optional[schema.AccessTokenPayload]:
    """
    Raises:
        jwt.ExpiredSignatureError:
        jwt.DecodeError:
        jwt.PyJWTError: otherwise
    """
    try:
        token_payload: schema.AccessTokenPayload = get_access_token_payload(access_token=token.split(" ")[-1])
        return token_payload
    except:
        raise HTTPException(status_code=401, detail=["wrong token"])
