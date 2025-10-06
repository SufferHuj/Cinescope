from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Union
import datetime


class MovieData(BaseModel):
    """Модель данных для создания и обновления фильма.
    
    Используется для передачи данных при создании нового фильма
    или обновлении существующего через API.
    """
    
    name: str = Field(min_length=1, max_length=255, description="Название фильма")
    description: str = Field(min_length=1, description="Описание фильма")
    price: int = Field(ge=0, description="Цена фильма в копейках")
    genreId: int = Field(ge=1, description="Идентификатор жанра фильма")
    imageUrl: Optional[str] = Field(default=None, description="URL изображения фильма")
    location: Optional[str] = Field(default=None, description="Местоположение показа")
    published: Optional[bool] = Field(default=True, description="Статус публикации фильма")
    rating: Optional[float] = Field(default=None, ge=0, le=10, description="Рейтинг фильма от 0 до 10")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("price")
    def validate_price(cls, value: int) -> int:
        """Валидатор для цены фильма.
        Проверяет, что цена является положительным числом.
        Args:
            value: Цена фильма в копейках
        Returns:
            int: Валидная цена
        Raises:
            ValueError: Если цена отрицательная
        """
        if value < 0:
            raise ValueError("Цена фильма не может быть отрицательной")
        return value


class CreateMovieResponse(BaseModel):
    """Модель ответа при создании нового фильма.
    
    Содержит информацию о созданном фильме,
    включая присвоенный идентификатор и все переданные данные.
    """
    
    id: int = Field(description="Уникальный идентификатор фильма")
    name: str = Field(min_length=1, max_length=255, description="Название фильма")
    description: str = Field(min_length=1, description="Описание фильма")
    price: int = Field(ge=0, description="Цена фильма в копейках")
    genreId: int = Field(ge=1, description="Идентификатор жанра фильма")
    imageUrl: Optional[str] = Field(default=None, description="URL изображения фильма")
    location: Optional[str] = Field(default=None, description="Местоположение показа")
    published: Optional[bool] = Field(default=True, description="Статус публикации фильма")
    rating: Optional[float] = Field(default=None, ge=0, le=10, description="Рейтинг фильма от 0 до 10")
    createdAt: Optional[str] = Field(default=None, description="Дата и время создания фильма в формате ISO8601")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        """Валидатор для поля createdAt.
        Проверяет, что дата создания соответствует формату ISO8601.
        Args:
            value: Строка с датой в формате ISO8601
        Returns:
            str: Валидная строка с датой
        Raises:
            ValueError: Если формат даты некорректный
        """
        if value is not None:
            try:
                datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Некорректный формат даты и времени. Ожидается ISO8601")
        return value


class GetMovieResponse(BaseModel):
    """Модель ответа при получении информации о фильме.
    
    Расширенная версия CreateMovieResponse с дополнительными полями
    для отображения полной информации о фильме.
    """
    
    id: int = Field(description="Уникальный идентификатор фильма")
    name: str = Field(min_length=1, max_length=255, description="Название фильма")
    description: str = Field(min_length=1, description="Описание фильма")
    price: int = Field(ge=0, description="Цена фильма в копейках")
    genreId: int = Field(ge=1, description="Идентификатор жанра фильма")
    imageUrl: Optional[str] = Field(default=None, description="URL изображения фильма")
    location: Optional[str] = Field(default=None, description="Местоположение показа")
    published: Optional[bool] = Field(default=True, description="Статус публикации фильма")
    rating: Optional[float] = Field(default=None, ge=0, le=10, description="Рейтинг фильма от 0 до 10")
    createdAt: Optional[str] = Field(default=None, description="Дата и время создания фильма в формате ISO8601")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        """Валидатор для поля createdAt.
        Проверяет, что дата создания соответствует формату ISO8601.
        Args:
            value: Строка с датой в формате ISO8601
        Returns:
            str: Валидная строка с датой
        Raises:
            ValueError: Если формат даты некорректный
        """
        if value is not None:
            try:
                datetime.datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Некорректный формат даты и времени. Ожидается ISO8601")
        return value


class GetMoviesResponse(BaseModel):
    """Модель ответа при получении списка фильмов с пагинацией.
    
    Используется для возврата списка фильмов с метаданными
    о пагинации и фильтрации.
    """

    movies: List[GetMovieResponse] = Field(description="Список фильмов на текущей странице")
    count: Optional[int] = Field(default=None, ge=0, description="Общее количество фильмов")
    page: Optional[int] = Field(default=None, ge=1, description="Номер текущей страницы")
    pageSize: Optional[int] = Field(default=None, ge=1, description="Размер страницы")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DeleteMovieResponse(BaseModel):
    """Модель ответа при удалении фильма.
    
    Содержит информацию об успешном удалении фильма
    или сообщение об ошибке.
    """
    
    message: str = Field(description="Сообщение о результате операции удаления")
    deletedMovieId: Optional[int] = Field(default=None, description="ID удаленного фильма")
    success: bool = Field(default=True, description="Статус успешности операции")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MovieFilterParams(BaseModel):
    """Модель параметров для фильтрации фильмов.
    
    Используется для передачи параметров фильтрации
    при получении списка фильмов через API.
    """
    
    page: Optional[int] = Field(default=1, ge=1, description="Номер страницы")
    pageSize: Optional[int] = Field(default=10, ge=1, le=100, description="Размер страницы")
    minPrice: Optional[int] = Field(default=None, ge=0, description="Минимальная цена фильма")
    maxPrice: Optional[int] = Field(default=None, ge=0, description="Максимальная цена фильма")
    locations: Optional[str] = Field(default=None, description="Местоположение показа")
    published: Optional[bool] = Field(default=None, description="Статус публикации")
    genreId: Optional[int] = Field(default=None, ge=1, description="Идентификатор жанра")
    order: Optional[str] = Field(default=None, description="Порядок сортировки")
    createdAt: Optional[str] = Field(default=None, description="Фильтр по дате создания")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("minPrice", "maxPrice")
    def validate_price_range(cls, value: int, info) -> int:
        """Валидатор для диапазона цен.
        Проверяет, что минимальная цена не превышает максимальную.
        Args:
            value: Значение цены
            info: Информация о других полях модели
        Returns:
            int: Валидное значение цены
        Raises:
            ValueError: Если минимальная цена больше максимальной
        """
        if value is not None and value < 0:
            raise ValueError("Цена не может быть отрицательной")
        
        # Проверяем соотношение min и max цен
        if info.field_name == "maxPrice" and "minPrice" in info.data:
            min_price = info.data["minPrice"]
            if min_price is not None and value is not None and min_price > value:
                raise ValueError("Минимальная цена не может быть больше максимальной")
        
        return value


class MovieErrorResponse(BaseModel):
    """Модель ответа при возникновении ошибки в операциях с фильмами.
    
    Стандартизированный формат для возврата информации об ошибках
    при работе с API фильмов.
    """
    
    error: Optional[str] = Field(default=None, description="Сообщение об ошибке")
    message: Optional[Union[str, List[str]]] = Field(default=None, description="Дополнительное сообщение об ошибке")
    statusCode: Optional[int] = Field(default=None, description="HTTP статус код")
    movieId: Optional[int] = Field(default=None, description="ID фильма, связанного с ошибкой")

    model_config = ConfigDict(arbitrary_types_allowed=True)
