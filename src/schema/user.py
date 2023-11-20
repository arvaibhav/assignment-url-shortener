from pydantic import BaseModel, constr, Field
from src.schema.auth import UserJWTAuthToken


class UserProfile(BaseModel):
    username: str
    email: str
    auth_token: UserJWTAuthToken


class UserAuthRequestSchema(BaseModel):
    username: str
    password: constr(max_length=48) = Field(
        ...,
        description="The user's password. Must be no more than 48 characters.",
        min_length=8,
    )


class UserSignupRequestSchema(UserAuthRequestSchema):
    email: str
