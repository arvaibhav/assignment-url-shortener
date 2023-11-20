import asyncio
from src.db.connection import get_db_client, close_connection, connect_and_init_db
from src.db.models.base import BaseDBModel


async def run_migrations():
    print("started")
    await connect_and_init_db()
    db_client = await get_db_client()
    print("doing schema update")
    for subclass in BaseDBModel.__subclasses__():
        print(f"Running migration for {subclass.__name__}")
        await subclass.db_migration(db_client)

    print(await db_client.list_collection_names())
    await close_connection()


if __name__ == "__main__":
    asyncio.run(run_migrations())
