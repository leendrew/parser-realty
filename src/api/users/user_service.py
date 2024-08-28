from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import (
  Depends,
  HTTPException,
)
from sqlalchemy import select
from src.shared import (
  BaseService,
  Logger,
)
from src.models.user_model import UserModel

logger = Logger().get_instance()

class UserService(BaseService):
  async def get_all(self) -> Sequence[UserModel]:
    stmt = select(UserModel)
    users = await self.session.scalars(stmt)

    return users.all()

  async def get_one(
    self,
    user_id: UUID,
  ) -> UserModel:
    stmt = (
      select(UserModel)
      .where(UserModel.id == user_id)
    )

    user = await self.session.scalar(stmt)
    if not user:
      logger.error(f"Пользователь с id \"{id}\" отсутствует")

      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Пользователь не найден",
      )

    return user

UserServiceDependency = Annotated[UserService, Depends()]
