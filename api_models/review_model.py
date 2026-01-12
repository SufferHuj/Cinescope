from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class CreateReviewResponse(BaseModel):
    """ Модель ответа при создании отзыва к фильму """
    
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
    """ Модель ответа при получении отзыва к фильму """
    
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
    """ Модель ответа при обновлении отзыва к фильму """
    
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
    """ Модель ответа при скрытии или показе отзыва к фильму """
    
    userId: str = Field(..., description="ID пользователя")
    text: str = Field(..., description="Текст отзыва")
    rating: int = Field(..., ge=1, le=5, description="Рейтинг фильма")
    createdAt: str = Field(..., description="Дата создания отзыва")
    user: dict = Field(..., description="Информация о пользователе")
    
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )
