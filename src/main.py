from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from contextlib import asynccontextmanager
import uvicorn
from .config import config
from .shared import db_service
from .api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
  # startup
  yield
  # shutdown
  await db_service.dispose()

app = FastAPI(
  default_response_class=ORJSONResponse,
  lifespan=lifespan,
)

app.include_router(
  api_router,
)

def main():
  uvicorn.run(
    "src.main:app",
    host=config.app.host,
    port=config.app.port,
    reload=True,
    workers=config.app.workers,
  )

if __name__ == "__main__":
  main()
