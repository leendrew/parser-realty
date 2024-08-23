from fastapi import APIRouter
from .parsing_results import parsing_result_router

api_router = APIRouter(
  prefix="/api",
)

