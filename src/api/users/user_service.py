from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import (
  Depends,
  HTTPException,
)
from sqlalchemy import (
  select,
  delete,
)
from src.shared import (
  Logger,
  BaseService,
)
from src.models.user_model import UserModel

logger = Logger().get_instance()

class UserService(BaseService):
  async def create_one(self) -> UserModel:
    model = UserModel()
    try:
      self.session.add(model)
      await self.session.commit()
      await self.session.refresh(model)

      return model

    except Exception:
      await self.session.rollback()

      logger.exception(f"Ошибка при создании пользователя")
      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Ошибка при создании пользователя",
      )

  async def get_all(self) -> Sequence[UserModel]:
    stmt = select(UserModel)
    users = await self.session.scalars(stmt)

    return users.all()

  async def get_one(
    self,
    id: UUID,
  ) -> UserModel | None:
    stmt = (
      select(UserModel)
      .where(UserModel.id == id)
    )

    user = await self.session.scalar(stmt)

    return user
  
  async def delete_one(
    self,
    id: UUID,
  ) -> UserModel | None:
    stmt = (
      delete(UserModel)
      .where(UserModel.id == id)
      .returning(UserModel)
    )

    try:
      result = await self.session.scalar(stmt)
      await self.session.commit()

      return result

    except Exception:
      await self.session.rollback()

      logger.exception(f"Ошибка при удалении пользователя с id \"{id}\"")
      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail="Ошибка при удалении пользователя",
      )

UserServiceDependency = Annotated[UserService, Depends()]
