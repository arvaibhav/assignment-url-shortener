from typing import Optional

from src.db.models import User
from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_user(
    db_client: AsyncIOMotorDatabase, username: str, password_hash: str, email: str
) -> User:
    user_dict = {"username": username, "password_hash": password_hash, "email": email}
    result = await db_client.get_collection(User.collection_name).insert_one(user_dict)
    return User(**user_dict, id=str(result.inserted_id))


async def get_user_by_username(
    db_client: AsyncIOMotorDatabase, username: str
) -> Optional[User]:
    user_data = await db_client.get_collection(User.collection_name).find_one(
        {"username": username}
    )
    if user_data:
        user_data["id"] = str(user_data.pop("_id"))
        return User(**user_data)
    return None
