from pydantic import BaseModel


class AccessTokenPayload(BaseModel):
    user_id: str
    token_id: int = None


class RefreshTokenPayload(BaseModel):
    user_id: str
    token_id: str = None


class UserJWTAuthToken(BaseModel):
    token_type: str = "bearer"
    access_token: str
    refresh_token: str
    expires_in_sec: int
    refresh_expires_in: int
