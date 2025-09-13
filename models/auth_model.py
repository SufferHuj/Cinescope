from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from constants import Roles
from typing import Optional, List
import datetime


class TestUserData(BaseModel):
    email: str = Field(pattern="@")
    fullName: str
    password: str = Field(min_length=8)
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Повторите пароль")
    roles: List[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    @field_serializer('roles')
    def serialize_roles(self, roles: List[Roles]) -> List[str]:
        return [role.value for role in roles]

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    roles: List[Roles]
    verified: Optional[bool] = None
    createdAt: str = Field(default=None, description="Дата и время создания пользователя в формате ISO8601")
    banned: Optional[bool] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        if value is not None:
            try:
                datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Некорректный формат даты и времени. Ожидается ISO8601")
        return value


class LoginUserResponse(BaseModel):
    accessToken: str
    refreshToken: str
    user: RegisterUserResponse

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ErrorResponse(BaseModel):
    error: str = Field(description="Сообщение об ошибке")
    message: Optional[str] = Field(default=None, description="Дополнительное сообщение об ошибке")
    statusCode: Optional[int] = Field(default=None, description="HTTP статус код")

    model_config = ConfigDict(arbitrary_types_allowed=True)