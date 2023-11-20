from enum import Enum
from fastapi import Header
from pydantic import BaseModel


class BaseHeader(BaseModel):
    user_agent: str


class UserAgenEnum(str, Enum):
    server = "server"
    android = "android"
    web = "web"


def user_common_headers(user_agent: UserAgenEnum = Header(default=UserAgenEnum.server)):
    return BaseHeader(user_agent=user_agent)
