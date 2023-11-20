from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.router import base_router
from src.db.connection import close_connection, connect_and_init_db

app = FastAPI(
    title="Url Shorter Service",
)
# App LifeCycle
app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("shutdown", close_connection)

# Middlewares
# 1.CORS
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
)

# Base Router
app.include_router(base_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
