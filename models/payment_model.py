from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
import datetime


class CreatePaymentResponse(BaseModel):
    """Модель ответа при создании платежа.
    
    Содержит информацию о результате обработки платежа,
    включая статус операции и дополнительные данные.
    """
    
    status: str = Field(description="Статус платежа (SUCCESS, FAILED, PENDING)")
    id: Optional[str] = Field(default=None, description="Уникальный идентификатор платежа")
    amount: Optional[int] = Field(default=None, description="Сумма платежа")
    movieId: Optional[int] = Field(default=None, description="Идентификатор фильма")
    userId: Optional[str] = Field(default=None, description="Идентификатор пользователя")
    createdAt: Optional[str] = Field(default=None, description="Дата и время создания платежа в формате ISO8601")

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


class PaymentInfo(BaseModel):
    """Модель информации о платеже.
    
    Расширенная модель платежа с полной информацией
    для отображения в списках и детальных представлениях.
    """
    
    id: int = Field(description="Уникальный идентификатор платежа")
    status: str = Field(description="Статус платежа")
    amount: int = Field(gt=0, description="Сумма платежа")
    total: int = Field(gt=0, description="Общая сумма платежа")
    movieId: int = Field(gt=0, description="Идентификатор фильма")
    userId: str = Field(description="Идентификатор пользователя")
    createdAt: str = Field(description="Дата и время создания платежа в формате ISO8601")
    movie: Optional[dict] = Field(default=None, description="Информация о фильме")
    user: Optional[dict] = Field(default=None, description="Информация о пользователе")

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


class GetAllPaymentsResponse(BaseModel):
    """Модель ответа при получении всех платежей с пагинацией.
    
    Используется для возврата списка всех платежей с метаданными
    о пагинации (текущая страница, размер страницы, общее количество).
    """
    
    payments: List[PaymentInfo] = Field(description="Список платежей на текущей странице")
    count: int = Field(ge=0, description="Общее количество платежей")
    page: int = Field(ge=1, description="Номер текущей страницы")
    pageSize: int = Field(ge=1, description="Размер страницы")
    pageCount: int = Field(ge=1, description="Общее количество страниц")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class PaymentErrorResponse(BaseModel):
    """Модель ответа при возникновении ошибки в платежной системе.
    
    Стандартизированный формат для возврата информации об ошибках
    платежных операций с детализацией причин неудачи.
    """
    
    error: Optional[str] = Field(default=None, description="Тип ошибки")
    message: Optional[str] = Field(default=None, description="Сообщение об ошибке")
    statusCode: Optional[int] = Field(default=None, description="HTTP статус код")
    details: Optional[dict] = Field(default=None, description="Дополнительные детали ошибки")

    model_config = ConfigDict(arbitrary_types_allowed=True)
    