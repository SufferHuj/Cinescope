from pydantic import BaseModel, Field, ConfigDict


class CreateGenreResponse(BaseModel):
    """Модель ответа при создании нового жанра.
    
    Содержит информацию о созданном жанре,
    включая присвоенный идентификатор и название.
    """
    
    id: int = Field(description="Уникальный идентификатор жанра")
    name: str = Field(min_length=1, max_length=100, description="Название жанра")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GetGenreResponse(BaseModel):
    """Модель ответа при получении информации о жанре.
    
    Содержит полную информацию о жанре, включая его идентификатор и название.
    Используется для ответов на запросы получения жанра по ID или списка жанров.
    """
    
    id: int = Field(description="Уникальный идентификатор жанра")
    name: str = Field(min_length=1, max_length=100, description="Название жанра")

    model_config = ConfigDict(arbitrary_types_allowed=True)