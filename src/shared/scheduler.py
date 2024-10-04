from asyncio import create_task
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.parsing.parsing_service import ParsingService
from src.api.search_links.search_link_types import SearchType
from .logger import Logger

logger = Logger().get_instance()

scheduler = AsyncIOScheduler()

cron_interval_by_search_type_map = {
  SearchType.rent: {
    "minute": "*/30",
  },
  SearchType.purchase: {
    "minute": "0",
    "hour": "3",
  },
}

async def parse_rent_job() -> None:
  parsing_service = ParsingService()
  print("start job rent")
  create_task(parsing_service.dispatch(SearchType.rent))

async def parse_purchase_job() -> None:
  parsing_service = ParsingService()
  print("start job purchase")
  create_task(parsing_service.dispatch(SearchType.purchase))

scheduler.add_job(
  parse_rent_job,
  "cron",
  minute="*/1",
)

# scheduler.print_jobs()
