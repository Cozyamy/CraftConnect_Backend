from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from configurations.config import settings
from configurations.db import engine
from routes.user_route import user_router
from routes.category_route import category_router
from routes.artisan_route import artisan_router
from routes.service_route import service_router
from sqlmodel import SQLModel
import logging

app = FastAPI(
    title = settings.PROJECT_NAME,
    description = settings.PROJECT_DESCRIPTION,
    version = "1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix=settings.API_V1_STR)             
app.include_router(category_router, prefix=settings.API_V1_STR)
app.include_router(artisan_router, prefix=settings.API_V1_STR)
app.include_router(service_router, prefix=settings.API_V1_STR)

@app.get(settings.API_V1_STR, include_in_schema=False)
def root() -> JSONResponse:
    return JSONResponse(status_code=200, content={"message": "Welcome to CraftConnect Server"})

@app.on_event("startup")
def on_startup():
    logger = logging.getLogger(__name__)
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")