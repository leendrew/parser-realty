from typing import (
  AsyncGenerator,
  Annotated,
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
  create_async_engine,
  async_sessionmaker,
  AsyncEngine,
  AsyncSession,
)
from src.config import (
  config,
  DbConfig,
)

class DbService:
  def __init__(
    self,
    db_config: DbConfig,
  ) -> None:
    self.engine: AsyncEngine = create_async_engine(
      url=str(db_config.url),
      echo=db_config.echo,
      echo_pool=db_config.echo_pool,
      pool_size=db_config.pool_size,
      max_overflow=db_config.max_overflow,
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

db_service = DbService(config.db)

SessionDependency = Annotated[AsyncSession, Depends(db_service.session)]
