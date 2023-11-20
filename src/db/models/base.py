from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class BaseDBModel(ABC, BaseModel):
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    @property
    def collection_name(cls):
        return cls.__name__.lower()

    @staticmethod
    @abstractmethod
    def db_migration(db_client: AsyncIOMotorDatabase):
        ...

    class Config:
        extra = "ignore"
