from fastapi import APIRouter
from .search_link_service import SearchLinkServiceDependency
from .search_link_dtos import (
  CreateOnePayloadDto,
  GetAllByQueryDtoDependency,
  EditOnePayloadDto,
)
from ..users.user_service import UserServiceDependency

router = APIRouter(
  prefix="/search-links",
)

@router.post("/")
async def create_one(
  search_link_service: SearchLinkServiceDependency,
  user_service: UserServiceDependency,
  payload: CreateOnePayloadDto,
):
  user = await user_service.get_one(user_id=payload.user_id)
  result = await search_link_service.create_one_to_user(
    link=payload.link,
    source_name=payload.source_name,
    user=user,
  )

  return result

@router.get("/")
async def get_all(
  search_link_service: SearchLinkServiceDependency,
  query: GetAllByQueryDtoDependency,
):
  result = await search_link_service.get_all_by(**query.model_dump())

  return result

@router.patch("/{id}")
async def edit_one(
  search_link_service: SearchLinkServiceDependency,
  id: int,
  payload: EditOnePayloadDto,
):
  result = await search_link_service.edit_one(
    id=id,
    is_active=payload.is_active,
  )

  return result

@router.delete("/{id}")
async def delete_one(
  search_link_service: SearchLinkServiceDependency,
  id: int,
):
  result = await search_link_service.delete_one(id=id)

  return result
