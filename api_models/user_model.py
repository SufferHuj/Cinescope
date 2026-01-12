from pydantic import BaseModel, Field, field_validator, ConfigDict
from constants import Roles
from typing import Optional, List
import datetime


class CreateUserResponse(BaseModel):
    """ Модель ответа при создании нового пользователя """
    
    id: str  # Уникальный идентификатор пользователя
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]  # Список ролей пользователя
    verified: Optional[bool] = None  # Статус верификации email
    banned: Optional[bool] = None  # Статус блокировки пользователя

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GetUserResponse(BaseModel):
    """ Модель ответа при получении информации о пользователе """
    
    id: str  # Уникальный идентификатор пользователя
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]  # Список ролей пользователя
    verified: Optional[bool] = None  # Статус верификации email
    banned: Optional[bool] = None  # Статус блокировки пользователя
    createdAt: Optional[str] = Field(default=None, description="Дата и время создания пользователя в формате ISO8601")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        """ Валидатор для поля createdAt. Проверяет, что дата создания соответствует формату ISO8601 """

        if value is not None:
            try:
                datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Некорректный формат даты и времени. Ожидается ISO8601")
        return value


class GetUsersResponse(BaseModel):
    """ Модель ответа при получении списка пользователей с пагинацией """

    users: List[GetUserResponse]  # Список пользователей на текущей странице
    count: int = Field(ge=0, description="Общее количество пользователей")
    page: int = Field(ge=1, description="Номер текущей страницы")
    pageSize: int = Field(ge=1, description="Размер страницы")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UpdateUserResponse(BaseModel):
    """ Модель ответа при обновлении информации о пользователе """
    
    id: Optional[str] = None  # Идентификатор пользователя (может быть None)
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]  # Обновленный список ролей пользователя
    verified: Optional[bool] = None  # Статус верификации email
    banned: Optional[bool] = None  # Статус блокировки пользователя
    createdAt: Optional[str] = Field(default=None, description="Дата и время создания пользователя в формате ISO8601")

    model_config = ConfigDict(arbitrary_types_allowed=True)
    