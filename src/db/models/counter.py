from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.db.models.base import BaseDBModel


class LastCounterRange(BaseDBModel):
    last_number: int

    @staticmethod
    async def db_migration(db_client: AsyncIOMotorDatabase):
        if (
            LastCounterRange.collection_name
            not in await db_client.list_collection_names()
        ):
            await db_client.create_collection(LastCounterRange.collection_name)
        await db_client.user.create_index("last_number")


class AppCounterReference(BaseDBModel):
    starts_from: int
    ends_at: int
    last_commits_at: int
    is_active: bool = True

    @staticmethod
    async def db_migration(db_client: AsyncIOMotorDatabase):
        if (
            LastCounterRange.collection_name
            not in await db_client.list_collection_names()
        ):
            await db_client.create_collection(LastCounterRange.collection_name)
