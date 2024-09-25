from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from .logger import Logger

logger = Logger().get_instance()

scheduler = AsyncIOScheduler()

# scheduler.print_jobs()
