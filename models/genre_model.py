from pydantic import BaseModel, Field, ConfigDict


class CreateGenreResponse(BaseModel):
    """ Модель ответа при создании нового жанра """
    
    id: int = Field(description="Уникальный идентификатор жанра")
    name: str = Field(min_length=1, max_length=100, description="Название жанра")

    model_config = ConfigDict(arbitrary_types_allowed=True)


class GetGenreResponse(BaseModel):
    """ Модель ответа при получении информации о жанре """
    
    id: int = Field(description="Уникальный идентификатор жанра")
    name: str = Field(min_length=1, max_length=100, description="Название жанра")

    model_config = ConfigDict(arbitrary_types_allowed=True)