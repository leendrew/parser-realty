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
from src.shared import BaseService
from src.models.user_model import UserModel

class UserService(BaseService):
  async def get_all(self) -> Sequence[UserModel]:
    stmt = select(UserModel)
    users = await self.session.scalars(stmt)

    return users.all()

  async def get_one(self, user_id: UUID) -> UserModel:
    stmt = select(UserModel).where(UserModel.id == user_id)
    user = await self.session.scalar(stmt)
    if not user:
      # TODO: log user with id does not exist
      print(f"Пользователь с id \"{id}\" отсутствует")

      raise HTTPException(
        status_code=400,
        detail="Пользователь с таким id отсутствует",
      )

    return user

UserServiceDependency = Annotated[UserService, Depends()]