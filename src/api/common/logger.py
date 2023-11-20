from fastapi import Header, Request
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/api.log', maxBytes=10000, backupCount=3),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def log_request_data(request: Request, user_agent: str = Header(None)):
    client_ip = request.client.host
    time_of_access = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    url_path = request.url.path

    # Log the details
    logger.info(
        f"Client IP: {client_ip}, "
        f"User Agent: {user_agent},"
        f" Time of Access: {time_of_access}, "
        f"URL Path: {url_path}"
    )
