from pydantic import BaseModel, Field, field_validator, ConfigDict
from constants import Roles
from typing import Optional, List
import datetime


class CreateUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GetUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    createdAt: Optional[str] = Field(default=None, description="Дата и время создания пользователя в формате ISO8601")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        if value is not None:
            try:
                datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Некорректный формат даты и времени. Ожидается ISO8601")
        return value


class GetUsersResponse(BaseModel):
    users: List[GetUserResponse]
    count: int = Field(ge=0, description="Общее количество пользователей")
    page: int = Field(ge=1, description="Номер текущей страницы")
    pageSize: int = Field(ge=1, description="Размер страницы")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UpdateUserResponse(BaseModel):
    id: Optional[str] = None
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    createdAt: Optional[str] = Field(default=None, description="Дата и время создания пользователя в формате ISO8601")

    model_config = ConfigDict(arbitrary_types_allowed=True)