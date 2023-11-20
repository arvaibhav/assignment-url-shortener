from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import field_validator
from src.db.models.base import BaseDBModel
from src.config import APP_CONFIG


class UserUrl(BaseDBModel):
    base_url: str
    short_url_index: str
    user_id: str
    max_retrieval: int = -1  # -1 means infinite
    expires_at: datetime

    @field_validator("max_retrieval")
    @classmethod
    def validate_max_retrieval(cls, value):
        if value != -1 and value <= 0:
            raise ValueError(
                "max_retrieval must be a positive number or -1 for infinite"
            )
        return value

    @staticmethod
    async def db_migration(db_client: AsyncIOMotorDatabase):
        if UserUrl.collection_name not in await db_client.list_collection_names():
            await db_client.create_collection(UserUrl.collection_name)
        await db_client.user.create_index("user_id")
        await db_client.user.create_index("short_url_index")

    @property
    def short_url(self):
        return f"{APP_CONFIG.domain}/{self.short_url_index}"
