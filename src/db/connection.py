import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.config import APP_CONFIG


class DB:
    __client: AsyncIOMotorClient = None
    __client_lock = asyncio.Lock()

    __database: AsyncIOMotorDatabase = None
    __database_lock = asyncio.Lock()

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        if cls.__client is None:
            async with cls.__client_lock:
                cls.__client = AsyncIOMotorClient(
                    APP_CONFIG.mongo_config.url,
                    username=APP_CONFIG.mongo_config.username,
                    password=APP_CONFIG.mongo_config.password,
                )
        return cls.__client

    @classmethod
    async def close_connection(cls):
        async with cls.__database_lock:
            cls.__client.close()
            cls.__client = None

    @classmethod
    async def check_health(cls):
        try:
            client = await cls.get_client()
            print(await client.server_info())
            return "true"
        except Exception as e:
            return "false"

    @classmethod
    async def get_base_database(cls) -> AsyncIOMotorDatabase:
        if cls.__database is None:
            async with cls.__database_lock:
                if cls.__database is None:
                    client = await cls.get_client()
                    cls.__database = getattr(
                        client, APP_CONFIG.mongo_config.base_database
                    )
        return cls.__database


async def get_db_client() -> AsyncIOMotorDatabase:
    database = await DB.get_base_database()
    return database


async def connect_and_init_db():
    print("mongo init")
    await DB.get_client()


async def close_connection():
    print("closing connection")
    await DB.close_connection()
