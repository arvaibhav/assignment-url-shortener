# URL Shortener Application

## Tech Stack

- **Python (3.10):**
- **Ruff:** A Python linter and code formatter to ensure code quality and consistency.
- **pydantic-settings:** For managing application configurations in a structured manner. (src/configs)
- **FastAPI:** For building APIs with Python.
- **MongoDB:**
    - **Motor:** The async MongoDB driver for Python.
- **Uvicorn:** ASGI server implementation for Python.
- **JWT (JSON Web Tokens):**
    - For secure user authentication: to ensures that only authenticated users can access certain API endpoints.


## Basic Flow

1. **User Registration and Authentication:**
    - Users sign up and log in to the system.
2. **URL Shortening Request:**
    - Logged-in users can request to shorten URLs.
    - Request includes:
        - The original URL.
        - Expiry duration (from 1 hour to 1 year).
        - Maximum retrieval limit for the shortened URL.
3. **Shortened URL Management:**
    - Users can view a list of their shortened URLs and usage statistics.
4. **URL Redirection:**
    - Accessing a shortened URL (`domain/short_url_id`):
        - Middleware logs user's IP, user agent, and access time.
        - If URL is valid, within time and retrieval limit, redirects to the original URL.
        - Otherwise, returns a 404 error.

## Other Consideration

- Short Url format
    - `domain/{unique_id}`
        - unique_id : is combination of Base52 (only first digit) + Base62 encoding ( 26 A-Z, 26 a-z, and 0-9 ) 
        - 7 digits i.e 52 * 62 ** 6 possible indexes .
