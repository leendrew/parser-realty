from fastapi import APIRouter
from src.shared import Logger
from .parsing_result_service import ParsingResultServiceDependency
from ..search_links.search_link_service import SearchLinkServiceDependency
from ..search_links.search_link_types import SourceName
from ..users_search_links.user_search_link_service import UserSearchLinkServiceDependency
from src.parsing.parsing_service import ParsingServiceDependency

logger = Logger().get_instance()

from asyncio import create_task, gather

router = APIRouter(
  # prefix="/parsing-results",
  # TODO: перед деплоем удалить, вернуть то, что выше
  prefix="/test",
)

@router.get("/")
async def get_parsing_results(
  parsing_service: ParsingServiceDependency,
  parsing_result_service: ParsingResultServiceDependency,
  search_link_service: SearchLinkServiceDependency,
  user_search_link_service: UserSearchLinkServiceDependency,
):
  # UserSearchLinkModel with relationships
  # CityMetroStationModel

  # user_id = "0c44ed8c-2fd0-439f-9e73-84b5776c34ac"
  user_id = "ab7536cd-9b3a-4835-a315-aa523c91a0f4"
  # await parsing_result_service.create_many(result)
  # users_search_links = await user_search_link_service.get_all_by(
  #   user_id=user_id,
  #   is_link_active=True,
  # )

  links = await search_link_service.get_all_by(user_id=user_id, is_active=True)

  return links
  # logger.info(f"Создаю задачи")
  # all = []
  # for link in links:
  #   task = parsing_service.dispatcher(source=link.source_name, link=link.search_link)
  #   task2 = parsing_service.dispatcher(source=link.source_name, link=link.search_link)
  #   all.append(task)
  #   all.append(task2)
  # res = await gather(*all)
  # logger.info(f"Получил результаты")
  # return res