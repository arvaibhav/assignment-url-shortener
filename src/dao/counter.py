from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.config import APP_CONFIG
from src.db.connection import DB
from src.db.models import LastCounterRange, AppCounterReference


async def get_counter_range():
    mongo_client = await DB.get_client()
    async with await mongo_client.start_session() as session:
        # Fetch and update the last number in a transaction
        db_client = getattr(mongo_client, APP_CONFIG.mongo_config.base_database)
        last_counter_range = await db_client.get_collection(
            LastCounterRange.collection_name
        ).find_one_and_update(
            {},
            {"$inc": {"last_number": 10000}},
            return_document=True,
            upsert=True,
            session=session,
        )
        last_number = last_counter_range["last_number"]
        starts_from = last_number
        ends_at = last_number + 10000 - 1

        # Add new counter reference
        result = await db_client.get_collection(
            AppCounterReference.collection_name
        ).insert_one(
            {
                "starts_from": starts_from,
                "ends_at": ends_at,
                "last_commits_at": starts_from,
                "is_active": True,
            },
            session=session,
        )
        return {
            "starts_from": starts_from,
            "ends_at": ends_at,
            "ref_id": str(last_counter_range.pop("_id")),
        }


async def update_counter(ref_id: str, last_commits_at: int):
    mongo_client = await DB.get_client()
    db_client = getattr(mongo_client, APP_CONFIG.mongo_config.base_database)

    await db_client.get_collection(AppCounterReference.collection_name).update_one(
        {"ref_id": ObjectId(ref_id)}, {"$set": {"last_commits_at": last_commits_at}}
    )
