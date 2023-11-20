import time
from fastapi import Request, HTTPException
import random
import logging.config
from fastapi.responses import JSONResponse
import traceback

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next):
    request_id = random.randint(0, 10000)
    request_start_time = time.time()
    server_error = None
    request_body = await request.body()
    try:
        response = await call_next(request)
    except HTTPException as error_response:
        response = error_response
    except:
        server_error = traceback.format_exc()
        response = JSONResponse(status_code=500, content={"internalServerError": True})

    request_end_time = time.time()

    # Collect request and response information
    response.headers["X-Request-ID"] = str(request_id)
    log_data = {
        "asctime": time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime()
        ),  # Request time (UTC)
        "name": __name__,  # Logger name
        "levelname": "INFO",  # Log level (assuming INFO for middleware)
        "message": f"rid={request_id} completed_in={request_end_time - request_start_time:.3f}s",
        "request_time": request_end_time,  # Request end time (Linux way)
        "request_id": request_id,  # Request ID
        "request_method": request.method,  # Request method
        "request_header": dict(request.headers),  # Request headers
        "request_meta": {
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client": request.client,
            "request_body": request_body,
        },
        "response_body": response._info,  # Response body
        "response_header": dict(response._headers),  # Response headers
        "response_http_code": response.status_code,  # Response HTTP code
        "server_error": server_error,
    }
    severity = "info"
    if server_error:
        severity = "error"
    getattr(logger, severity)(log_data)
    return response
