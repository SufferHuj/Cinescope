from pydantic import BaseModel, Field, EmailStr
from constants import Roles
from typing import Optional


class TestUserData(BaseModel):
    email: str = Field(pattern="@") # либо EmailStr для лучшей валидации
    fullName: str
    password: str = Field(min_length=8)
    passwordRepeat: str = Field(min_length=8)
    roles: list[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None