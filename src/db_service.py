from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
  create_async_engine,
  async_sessionmaker,
  AsyncEngine,
  AsyncSession,
)
from .config import config

class DbService:
  def __init__(
    self,
    url: str,
    echo: bool = False,
    echo_pool: bool = False,
    pool_size: int = 5,
    max_overflow: int = 10,
  ) -> None:
    self.engine: AsyncEngine = create_async_engine(
      url=url,
      echo=echo,
      echo_pool=echo_pool,
      pool_size=pool_size,
      max_overflow=max_overflow,
    )
    self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
      bind=self.engine,
      autoflush=False,
      autocommit=False,
      expire_on_commit=False,
    )

  async def dispose(self) -> None:
    await self.engine.dispose()

  async def session(self) -> AsyncGenerator[AsyncSession, None]:
    async with self.session_factory() as session:
      yield session

db_service = DbService(
  url=str(config.db.url),
  echo=config.db.echo,
  echo_pool=config.db.echo_pool,
  pool_size=config.db.pool_size,
  max_overflow=config.db.max_overflow,
)
