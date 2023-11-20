from pydantic_settings import BaseSettings
import os

ENV_FILE = (
    ".env.production"
    if os.getenv("APP_ENV", "development").lower() == "production"
    else ".env.development"
)


class _JWTConfig(BaseSettings):
    token_expires_in: int = 60 * 60  # default 1 hour
    refresh_token_expires_in: int = 60 * 60 * 24 * 7  # default: 7 days

    class Config:
        env_prefix = "JWT_"
        env_file = ENV_FILE


class _MongoConfig(BaseSettings):
    username: str
    password: str
    url: str
    base_database: str

    class Config:
        env_prefix = "MONGO_DB_"
        env_file = ENV_FILE


class _BaseConfig(BaseSettings):
    jwt_config: _JWTConfig = _JWTConfig()
    mongo_config: _MongoConfig = _MongoConfig()

    class Config:
        env_file = ENV_FILE
        extra = "ignore"


class _SingletonConfig:
    __instance = None

    @classmethod
    @property
    def instance(cls) -> _BaseConfig:
        if cls.__instance is None:
            cls.__instance = _BaseConfig()
        return cls.__instance


APP_CONFIG: _BaseConfig = _SingletonConfig().instance
