from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Header
from starlette.responses import RedirectResponse

from src import schema
from src.core.counter import Counter
from src.dao.shorten_url import (
    create_shortern_url,
    get_and_increment_shorten_url,
    mark_shortern_url_inactive,
)
from src.db.connection import get_db_client
from src.utils.string_hasher import number_to_base62
from datetime import datetime
from src.api.common.authentication import get_auth_token_payload

router = APIRouter()


def clean_url(url):
    if url.startswith("www."):
        url = url[4:]

    url = url.rstrip("/")
    return url


@router.post("/generate", response_model=schema.ShortURLResponse)
async def generate_short_url(
    db_client=Depends(get_db_client),
    auth=Depends(get_auth_token_payload),
    *,
    url_input: schema.URLRequestInput,
):
    cleaned_url = clean_url(url_input.url)
    counter_number = await Counter().get_next()
    short_url_index = number_to_base62(counter_number)
    shortern_url_obj = await create_shortern_url(
        db_client,
        base_url=cleaned_url,
        short_url_index=short_url_index,
        user_id=url_input.user_id,
        max_retrieval=url_input.max_retrieval,
        expires_at=url_input.expires_at,
    )

    return schema.ShortURLResponse(
        base_url=cleaned_url,
        short_url=shortern_url_obj.short_url,
        expires_at=url_input.expires_at,
        created_at=shortern_url_obj.created_at,
        max_retrieval=url_input.max_retrieval,
    )


redirection_router = APIRouter()


@redirection_router.get("/{short_url_index}", response_model=schema.ShortURLResponse)
async def get_short_url(
    background_tasks: BackgroundTasks,
    db_client=Depends(get_db_client),
    *,
    short_url_index: str,
    user_agent: str = Header("server"),
):
    shortern_url_obj = await get_and_increment_shorten_url(db_client, short_url_index)

    if not shortern_url_obj or not shortern_url_obj.is_active:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if shortern_url_obj.usage_count == shortern_url_obj.max_retrieval:
        # so that other could not retrieve
        background_tasks.add_task(
            mark_shortern_url_inactive, db_client, short_url_index
        )
    if shortern_url_obj.expires_at < datetime.utcnow():
        background_tasks.add_task(
            mark_shortern_url_inactive, db_client, short_url_index
        )
        raise HTTPException(status_code=404, detail="Short URL Expired")

    return RedirectResponse(url=shortern_url_obj.base_url)
