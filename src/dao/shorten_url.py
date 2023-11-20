from datetime import datetime
from typing import Optional

from bson import ObjectId
from src.db.models import UserUrl
from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_shortern_url(
    db_client: AsyncIOMotorDatabase,
    base_url: str,
    short_url_index: str,
    user_id: str,
    max_retrieval: int,
    expires_at: datetime,
) -> UserUrl:
    user_url_dict = {
        "base_url": base_url,
        "short_url_index": short_url_index,
        "user_id": ObjectId(user_id),  # Convert user_id string to ObjectId
        "max_retrieval": max_retrieval,
        "expires_at": expires_at,
        "is_active": True,
    }
    result = await db_client.get_collection(UserUrl.collection_name).insert_one(
        user_url_dict
    )
    user_url_dict["user_id"] = str(user_url_dict["user_id"])
    return UserUrl(**user_url_dict, id=str(result.inserted_id))


async def get_shortern_url_by_index(
    db_client: AsyncIOMotorDatabase, short_url_index: str
) -> Optional[UserUrl]:
    url_data = await db_client.get_collection(UserUrl.collection_name).find_one(
        {"short_url_index": short_url_index, "is_active": True}
    )
    if url_data:
        url_data["id"] = str(url_data.pop("_id"))
        return UserUrl(**url_data)
    return None


async def get_and_increment_shorten_url(
    db_client: AsyncIOMotorDatabase, short_url_index: str
) -> Optional[UserUrl]:
    url_data = await db_client.get_collection(
        UserUrl.collection_name
    ).find_one_and_update(
        {"short_url_index": short_url_index, "is_active": True},
        {"$inc": {"usage_count": 1}},
        return_document=True,
    )

    if url_data:
        url_data["id"] = str(url_data.pop("_id"))
        url_data["user_id"] = str(url_data.pop("user_id", ""))
        return UserUrl(**url_data)
    return None


async def mark_shortern_url_inactive(
    db_client: AsyncIOMotorDatabase, short_url_index: str
):
    result = await db_client.get_collection(UserUrl.collection_name).update_one(
        {"short_url_index": short_url_index}, {"$set": {"is_active": False}}
    )
    return result.modified_count > 0  # Returns True if the document was updated


async def get_shortern_urls_for_user_id(db_client: AsyncIOMotorDatabase, user_id: str):
    cursor = db_client.get_collection(UserUrl.collection_name).find(
        {"user_id": ObjectId(user_id)}
    )
    return [UserUrl(**(await doc)) for doc in cursor]
