from asyncio import create_task
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
import uvicorn
from .config import (
  config,
  AppEnv,
)
from .shared import (
  db_service,
  queues,
  scheduler,
)
from .api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
  # startup
  create_task(queues.start())
  scheduler.start()
  yield
  # shutdown
  scheduler.shutdown()
  await queues.stop()
  await db_service.dispose()

app = FastAPI(
  default_response_class=ORJSONResponse,
  lifespan=lifespan,
)

app.include_router(
  api_router,
)

def main():
  reload_by_env = {
    AppEnv.development: True,
    AppEnv.production: False,
  }
  reload = reload_by_env[config.app.env]

  uvicorn.run(
    "src.main:app",
    host=config.app.host,
    port=config.app.port,
    reload=reload,
    workers=config.app.workers,
  )

if __name__ == "__main__":
  main()
