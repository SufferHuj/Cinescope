import logging

import pytest
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ValidationError, model_validator
from enum import Enum
from venv import logger
import json
import jsonschema
from models.auth_model import TestUserData
from fastapi import FastAPI


# def test_user_data_validation(test_user, creation_user_data):
#
#     # Создаем экземпляр модели из данных фикстуры Pydantic автоматически проверит типы и структуру
#     registration_model = TestUserData(**test_user)
#
#     # Проверяем, что опциональные поля, которых не было в фикстуре, получили значение None
#     assert registration_model.verified is None
#     assert registration_model.banned is None
#
#     # Переводим в JSON с exclude_unset=True и логируем
#     # exclude_unset=True исключит из JSON поля, которые не были явно заданы (verified и banned)
#     json_data_exclude_unset = registration_model.model_dump_json(exclude_unset=True, indent=4)
#     # Переводим JSON в Объект
#     json_to_obj_1 = TestUserData.model_validate_json(json_data_exclude_unset)
#
#     logger.info(f"\n\n--- JSON for test_user (exclude_unset=True) ---")
#     logger.info(json_data_exclude_unset)
#     logger.info(json_to_obj_1)
#     print(json_to_obj_1)
#
#     # Создаем экземпляр модели из второй фикстуры
#     creation_model = TestUserData(**creation_user_data)
#
#     # Проверяем, что поля установились корректно
#     assert creation_model.verified is True
#     assert creation_model.banned is False
#
#     # Переводим в JSON без exclude_unset=True и логируем
#     # В JSON будут включены все поля модели, включая verified и banned
#     json_creation_data = creation_model.model_dump_json(indent=4)
#     # Переводим JSON в Объект
#     json_to_obj_2 = TestUserData.model_validate_json(json_creation_data)
#
#     logger.info(f"\n\n--- JSON for creation_user_data (без exclude_unset) ---")
#     logger.info(json_creation_data)
#     logger.info(json_to_obj_2)
#
# # НОВЫЙ ТЕСТ: Проверка на короткий пароль
# def test_short_password_fails(test_user):
#     """
#     Проверяем, что модель выдаст ошибку, если пароль короче 8 символов.
#     """
#     invalid_data = test_user.copy()
#     invalid_data["password"] = "12345678" # Невалидный пароль
#
#     # Используем pytest.raises для "отлова" ожидаемого исключения
#     with pytest.raises(ValidationError) as exc_info:
#         TestUserData(**invalid_data) # Эта строка должна вызвать ошибку
#
# # НОВЫЙ ТЕСТ: Проверка на невалидный email
# def test_invalid_email_fails(test_user):
#
#     """
#     Проверяем, что модель выдаст ошибку на некорректный email.
#     """
#     invalid_data = test_user.copy()
#     invalid_data["email"] = "not-an-email" # Невалидный email
#
#     with pytest.raises(ValidationError) as exc_info:
#         TestUserData(**invalid_data)
#
#     assert "Invalid email address" in str(exc_info.value)
#
#
# class ProductType(str, Enum):
#     NEW = "new"
#     PREVIOUS_USE = "previous_use"
#
# class Manufacturer(BaseModel):
#     name: str
#     city: Optional[str] = None
#     street: Optional[str] = None
#
# class Product(BaseModel):
#     # поле name может иметь длину в диапазоне от 3 до 50 символов и является строкой
#     name: str = Field(..., min_length=3, max_length=50, description="Название продукта")
#     # поле price должно быть больше 0
#     price: float = Field(..., gt=0, description="Цена продукта")
#     # поле in_stock принимает булево значение и установится по умолчанию = False
#     in_stock: bool = Field(default=False, description="Есть ли в наличии")
#     # поле color должно быть строкой и принимает значение "black" по умолчанию
#     color: str = "black"
#     # поле year не обязательное. можно не указывать при создании обьекта
#     year: Optional[int] = None
#     # поле product принимает тип Enum (может содержать только 1 из его значений)
#     product: ProductType
#     # поле manufacturer принимает тип другой BaseModel
#     manufacturer: Manufacturer
#
# @pytest.mark.skip
# def test_product():
#     # Пример создания обьекта + в поле price передаём строку вместо числа
#     product = Product(name="Laptop", price="999.99", product=ProductType.NEW, manufacturer=Manufacturer(name="MSI"))
#     logger.info(f"{product=}")
#     # Output: product=Product(name='Laptop', price=999.99, in_stock=False, color='black', year=None, product=<ProductType.NEW: 'new'>, manufacturer=Manufacturer(name='MSI', city=None, street=None))
#
#     # Пример конвертации обьекта в json
#     json_data = product.model_dump_json(exclude_unset=True)
#     logger.info(f"{json_data=}")
#     # Output: json_data='{"name":"Laptop","price":999.99,"product":"new","manufacturer":{"name":"MSI"}}'
#
#     # Пример конвертации json в обьект
#     new_product = Product.model_validate_json(json_data)
#     logger.info(f"{new_product=}")
#     # Output: new_product=Product(name='Laptop', price=999.99, in_stock=False, color='black', year=None, product=<ProductType.NEW: 'new'>, manufacturer=Manufacturer(name='MSI', city=None, street=None))
#
#
# class PostgresClient:
#     # Mock - заглушка вмеcто реального сервиса. делающего запрос в базу данных
#     @staticmethod
#     def get(key: str):
#         return None
#
# class Card(BaseModel):
#     pan: str = Field(..., min_length=16, max_length=16, description="Номер карты")
#     cvc: str = Field(...,  min_length=3, max_length=3)
#
#     @field_validator("pan")  # кастомный валидатор для проверки поля pan
#     def check_pan(cls, value: str) -> str:
#         """
#             не самый лучший пример. не стоит добавлять в валидаторы сложновесную логику
#             но данным примером хочется показать что кастомные валидаторы лучше использовать
#             для ситуаций которые невозможно проверить доступной логикой Field
#         """
#
#         """
#         Проверяем, есть ли карта в базе данных (здесь - в PostgresClient)
#         """
#         if PostgresClient.get(f'card_by_pan_{value}') is None:
#             raise ValueError("Такой карты не существует")
#         return value
# @pytest.mark.skip
# # Попытка создать объект с данными. отсутствующими в базе данных
# def test_field_validator():
#     try:
#         card = Card(pan="1234567890123456", cvc="123")
#         logger.info(card)
#     except ValidationError as e:
#         logger.info(f"Ошибка валидации: {e}")
#         raise
#
#
#
#
# class User2(BaseModel):
#     id: int
#     name: str
#     email: str
#     is_active: bool = True
# @pytest.mark.skip
# def test_model_json_schema():
#     # Генерируем JSON Schema
#     user_schema = User2.model_json_schema()
#     x = json.dumps(user_schema, indent=4, ensure_ascii=False)
#     logger.info("\n" + x)
#
#     # Данные для валидации
#     user2_data = {
#         "id": 1,
#         "name": "Alice",
#         "email": "alice@example.com",
#         "is_active": True
#     }
#
#     # Валидируем данные с использованием JSON Schema
#     try:
#         jsonschema.validate(user2_data, x)
#         logger.info("Данные валидны!")
#     except jsonschema.ValidationError as e:
#         logger.info("Ошибка валидации:", e)
#
#
#     app = FastAPI()
#
#     @app.post("/users/")
#     async def create_user(user: User2):
#         return user

# class TypeProduct(str, Enum):
#     Electronics = "Electronics"
#     Clothing = "Clothing"
#     KidsToy = "Toy"
#
# class Product(BaseModel):
#
#     name: str
#     price: float
#     in_stock: bool
#     type: TypeProduct
#
# def test_json_workout():
#
#     product = Product(name="LG", price=1000.9, in_stock="TRUE", type=TypeProduct.KidsToy)
#
#     serialize_json = product.model_dump_json()
#
#     logging.info(serialize_json)
#
#     invalid_json = Product.model_validate_json(serialize_json)
#
#     logging.info(invalid_json)

