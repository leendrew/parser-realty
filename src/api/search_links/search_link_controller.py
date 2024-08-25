from fastapi import APIRouter
from .search_link_service import SearchLinkServiceDependency
from .search_link_dtos import (
  CreateOnePayloadDto,
  GetAllByQueryDtoDependency,
)

router = APIRouter(
  prefix="/search-links",
)

@router.post("/")
async def create_one(
  search_link_service: SearchLinkServiceDependency,
  payload: CreateOnePayloadDto,
):
  result = await search_link_service.create_one_to_user(**payload.model_dump())

  return result

@router.get("/")
async def get_all(
  search_link_service: SearchLinkServiceDependency,
  query: GetAllByQueryDtoDependency,
):
  result = await search_link_service.get_all_by(**query.model_dump())

  return result
