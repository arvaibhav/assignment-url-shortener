from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class URLRequestInput(BaseModel):
    url: str
    expires_at: datetime  # Timestamp in UTC
    max_retrieval: int = Field(..., description="Positive number or -1 for infinite")
    user_id: str

    @field_validator("max_retrieval")
    @classmethod
    def validate_max_retrieval(cls, value):
        if value != -1 and value <= 0:
            raise ValueError(
                "max_retrieval must be a positive number or -1 for infinite"
            )
        return value


class ShortURLResponse(BaseModel):
    short_url: str
    expires_at: datetime
    created_at: datetime
    max_retrieval: int
    base_url: str
