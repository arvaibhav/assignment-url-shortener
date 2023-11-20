from fastapi import APIRouter, Depends
from src import schema
from src.dao.shorten_url import create_shortern_url
from src.db.connection import get_db_client
from src.utils.string_hasher import number_to_base62

router = APIRouter()


def clean_url(url):
    if url.startswith('www.'):
        url = url[4:]

    url = url.rstrip('/')
    return url


@router.post("/generate", response_model=schema.ShortURLResponse)
async def generate_short_url(
        db_client=Depends(get_db_client), *, url_input: schema.URLRequestInput
):
    cleaned_url = clean_url(url_input.url)
    counter_number = 1
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
