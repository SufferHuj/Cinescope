from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from constants import Roles
from typing import Optional, List, Union
import datetime


class TestUserData(BaseModel):
    """ Модель данных для тестирования пользователей """
    
    email: str = Field(pattern="@")  # Email с базовой валидацией
    fullName: str  # Полное имя пользователя
    password: str = Field(min_length=8)  # Пароль минимум 8 символов
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Повторите пароль")
    roles: List[Roles] = [Roles.USER]  # Роли пользователя, по умолчанию USER
    verified: Optional[bool] = None  # Статус верификации email
    banned: Optional[bool] = None  # Статус блокировки пользователя

    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    @field_serializer('roles')
    def serialize_roles(self, roles: List[Roles]) -> List[str]:
        """ Сериализатор для ролей пользователя """

        return [role.value for role in roles]

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        """ Валидатор для проверки совпадения паролей """

        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponse(BaseModel):
    """ Модель ответа при регистрации пользователя """
    
    id: str  # Уникальный идентификатор пользователя
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]  # Список ролей пользователя
    verified: Optional[bool] = None  # Статус верификации email
    createdAt: str = Field(default=None, description="Дата и время создания пользователя в формате ISO8601")
    banned: Optional[bool] = None  # Статус блокировки пользователя

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


class LoginUserResponse(BaseModel):
    """ Модель ответа при успешном входе в систему """
    
    accessToken: str  # JWT токен для доступа к API
    refreshToken: str  # Токен для обновления access токена
    user: RegisterUserResponse  # Информация о пользователе

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ErrorResponse(BaseModel):
    """ Модель ответа при возникновении ошибки """
    
    error: Optional[str] = Field(default=None, description="Сообщение об ошибке")
    message: Optional[Union[str, List[str]]] = Field(default=None, description="Дополнительное сообщение об ошибке")
    statusCode: Optional[int] = Field(default=None, description="HTTP статус код")

    model_config = ConfigDict(arbitrary_types_allowed=True)
    