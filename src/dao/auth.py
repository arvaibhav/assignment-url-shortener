from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

from src.db.models import UserAuth


async def create_user_auth(
    db_client: AsyncIOMotorDatabase, user_id: str, expires_in_sec: int
) -> UserAuth:
    user_auth_data = {"user_id": user_id, "expires_in_sec": expires_in_sec}
    result = await db_client.get_collection(UserAuth.collection_name).insert_one(
        user_auth_data
    )
    user_auth_data["id"] = str(result.inserted_id)
    return UserAuth(**user_auth_data)


async def get_user_auth_by_id(
    db_client: AsyncIOMotorDatabase, _id: str
) -> Optional[UserAuth]:
    obj_id = ObjectId(_id)  # Convert string to ObjectId
    user_auth_data = await db_client.get_collection(
        UserAuth.collection_name
    ).find_one(
        {"_id": obj_id}
    )
    if user_auth_data:
        user_auth_data['id'] = str(user_auth_data.pop('_id'))
        return UserAuth(**user_auth_data)
    return None
