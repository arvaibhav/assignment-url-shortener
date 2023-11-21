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

- Counter Mechanism for Unique and Ordered Base62 IDs
    1. **Counter Implementation:**
        - To achieve uniqueness, a counter mechanism is employed within the application.
        - The counter ensures that each generated ID is unique and ordered.
        - When a new short URL is requested, the counter provides the next available unique ID within its assigned range.
    2. **Reason for Range:**
        - Multi-server instances of the application can work concurrently without generating duplicate IDs.
        - Reduce the query cost to known last committed number.
    3. **Counter Initialization:**
        - At **application startup, the counter is initialized with its unique range.
        - For instance, a range of IDs from 10000 to 19999 might be assigned.
     4. **Data Models for Counter:**
        - In MongoDB, two data models are used to manage the counter mechanism:
            - **`LastCounterRange` Model:**
                - Stores the last number used in the counter.
                - Ensures that each counter range is unique.
            - **`AppCounterReference` Model:**
                - Represents the counter reference for each range.
                - Tracks the starting point, ending point, and last committed position within a range.
                - Is active or inactive based on usage.


## Project Structure

```
.
├── .env.development                # Environment-specific configurations (dev env p.o.v)
├── Dockerfile                      # Instructions to build the Docker image
├── docker-compose.yaml             # Defines multi-container Docker applications
├── requirements.txt                # Python App dependencies
├── run_docker.sh                   # Script to run Docker-related commands (setup env)
├── scripts
│   └── mongo_models_migrations.py  # MongoDB models migration scripts (auto migrate the models which are defined at src/db/models
└── src
    ├── api                         # API route definitions and logic
    │   ├── __init__.py
    │   ├── auth                    # Authentication-related routes
    │   │   ├── __init__.py
    │   │   └── router.py
    │   ├── common                  # Common functionalities (middlewares, logger, dependecies)
    │   │   ├── __init__.py
    │   │   ├── authentication.py
    │   │   ├── logger.py
    │   │   └── middlewares.py
    │   ├── router.py
    │   ├── url_shortener           # URL shortener specific routes
    │   │   ├── __init__.py
    │   │   └── router.py
    │   └── user                    # User management routes
    │       ├── __init__.py
    │       └── router.py
    ├── config.py                   # Configuration settings for the app
    ├── core                        # Core business logic and functionalities
    │   ├── __init__.py
    │   ├── counter.py
    │   └── user_auth.py
    ├── dao                         # Data Access Objects for database interactions
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── counter.py
    │   ├── shorten_url.py
    │   └── user.py
    ├── db                          # Database models and connection setup
    │   ├── __init__.py
    │   ├── connection.py
    │   └── models
    │       ├── __init__.py
    │       ├── auth.py
    │       ├── base.py
    │       ├── counter.py
    │       ├── shorten_url.py
    │       └── user.py
    ├── main.py                     # Main entry point for the application
    ├── schema                      # Pydantic schemas for request and response validation
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── url_shortner.py
    │   └── user.py
    └── utils                       # Utility functions and helpers
        ├── __init__.py
        ├── jwt_auth.py
        └── string_hasher.py
```

