from motor.motor_asyncio import AsyncIOMotorDatabase
from src.db.models.base import BaseDBModel


class User(BaseDBModel):
    username: str
    password_hash: str
    email: str

    @staticmethod
    async def db_migration(db_client: AsyncIOMotorDatabase):
        if User.collection_name not in await db_client.list_collection_names():
            await db_client.create_collection(User.collection_name)
        await db_client.user.create_index("username", unique=True)
