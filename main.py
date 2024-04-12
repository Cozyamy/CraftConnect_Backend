from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from configurations.config import settings
from configurations.db import engine
from routes.user_route import api_router
from sqlmodel import SQLModel

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

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get(settings.API_V1_STR, include_in_schema=False)
def root() -> JSONResponse:
    return JSONResponse(status_code=200, content={"message": "Welcome to CraftConnect Server"})

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)