from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional


class CreateReviewResponse(BaseModel):
    """
    Модель ответа при создании отзыва к фильму.
    
    Содержит информацию о созданном отзыве, включая ID пользователя,
    текст отзыва, рейтинг, дату создания и информацию о пользователе.
    
    Attributes:
        userId (str): Уникальный идентификатор пользователя
        text (str): Текст отзыва
        rating (int): Рейтинг фильма от 1 до 5
        createdAt (str): Дата и время создания отзыва в формате ISO
        user (dict): Информация о пользователе, создавшем отзыв
    """
    
    userId: str = Field(..., description="ID пользователя, создавшего отзыв")
    text: str = Field(..., description="Текст отзыва")
    rating: int = Field(..., ge=1, le=5, description="Рейтинг фильма")
    createdAt: str = Field(..., description="Дата создания отзыва")
    user: dict = Field(..., description="Информация о пользователе")
    
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class GetReviewResponse(BaseModel):
    """
    Модель ответа при получении отзыва к фильму.
    
    Используется для валидации ответа API при получении информации об отзыве.
    Содержит полную информацию об отзыве.
    
    Attributes:
        userId (int): ID пользователя, создавшего отзыв
        rating (int): Рейтинг фильма от 1 до 5
        text (str): Текст отзыва
        movieId (Optional[int]): ID фильма
        createdAt (Optional[str]): Дата и время создания отзыва
        updatedAt (Optional[str]): Дата и время последнего обновления отзыва
        isHidden (Optional[bool]): Флаг скрытия отзыва
        userName (Optional[str]): Имя пользователя, создавшего отзыв
    """
    
    userId: int = Field(..., description="ID пользователя, создавшего отзыв")
    rating: int = Field(..., ge=1, le=5, description="Рейтинг фильма")
    text: str = Field(..., description="Текст отзыва")
    movieId: Optional[int] = Field(None, description="ID фильма")
    createdAt: Optional[str] = Field(None, description="Дата создания отзыва")
    updatedAt: Optional[str] = Field(None, description="Дата обновления отзыва")
    isHidden: Optional[bool] = Field(None, description="Флаг скрытия отзыва")
    userName: Optional[str] = Field(None, description="Имя пользователя")
    
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True
    )


class UpdateReviewResponse(BaseModel):
    """
    Модель ответа при обновлении отзыва к фильму.
    
    Содержит информацию об обновленном отзыве, включая ID фильма,
    ID пользователя, статус скрытия, текст, рейтинг и дату создания.
    
    Attributes:
        movieId (int): Уникальный идентификатор фильма
        userId (str): Уникальный идентификатор пользователя
        hidden (bool): Статус скрытия отзыва
        text (str): Обновленный текст отзыва
        rating (int): Обновленный рейтинг фильма от 1 до 5
        createdAt (str): Дата и время создания отзыва в формате ISO
    """
    
    movieId: int = Field(..., description="ID фильма")
    userId: str = Field(..., description="ID пользователя")
    hidden: bool = Field(..., description="Статус скрытия отзыва")
    text: str = Field(..., description="Обновленный текст отзыва")
    rating: int = Field(..., ge=1, le=5, description="Обновленный рейтинг фильма")
    createdAt: str = Field(..., description="Дата создания отзыва")
    
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class HideShowReviewResponse(BaseModel):
    """
    Модель ответа при скрытии или показе отзыва к фильму.
    
    Содержит информацию об отзыве после операции скрытия/показа,
    включая ID пользователя, текст, рейтинг, дату создания и информацию о пользователе.
    
    Attributes:
        userId (str): Уникальный идентификатор пользователя
        text (str): Текст отзыва
        rating (int): Рейтинг фильма от 1 до 5
        createdAt (str): Дата и время создания отзыва в формате ISO
        user (dict): Информация о пользователе
    """
    
    userId: str = Field(..., description="ID пользователя")
    text: str = Field(..., description="Текст отзыва")
    rating: int = Field(..., ge=1, le=5, description="Рейтинг фильма")
    createdAt: str = Field(..., description="Дата создания отзыва")
    user: dict = Field(..., description="Информация о пользователе")
    
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )
