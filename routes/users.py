from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


users: APIRouter = APIRouter(prefix="/users", tags=["users"])
