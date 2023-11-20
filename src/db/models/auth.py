from motor.motor_asyncio import AsyncIOMotorDatabase
from src.db.models.base import BaseDBModel


class UserAuth(BaseDBModel):
    user_id: str
    is_evoked: bool = False
    expires_in_sec: int

    @property
    def token_id(self):
        return self.id

    @staticmethod
    async def db_migration(db_client: AsyncIOMotorDatabase):
        if UserAuth.collection_name not in await db_client.list_collection_names():
            await db_client.create_collection(UserAuth.collection_name)
        await db_client.user.create_index("user_id")
