# Cinescope 🎬

**Cinescope** - это проект автоматизации тестирования для сервиса, связанного с фильмами. Проект включает тестирование
API аутентификации, управления пользователями, работы с данными о фильмах и платежной системы.

## 🚀 Основные возможности

- ✅ **API тестирование** - автоматизированное тестирование REST API эндпоинтов
- 🔐 **Аутентификация** - тестирование процессов логина и регистрации
- 👥 **Управление пользователями** - тестирование CRUD операций с пользователями
- 🎭 **Работа с фильмами** - тестирование API для работы с фильмами и жанрами
- 💬 **Система отзывов** - тестирование функционала отзывов к фильмам
- 💳 **Платежная система** - тестирование API создания платежей
- 📊 **Генерация тестовых данных** - автоматическая генерация данных для тестов

## 🛠 Технологический стек

- **Python 3.8+** - основной язык программирования
- **pytest** - фреймворк для тестирования
- **requests** - HTTP клиент для API запросов
- **Pydantic** - валидация данных
- **Faker** - генерация тестовых данных

## 📁 Структура проекта

```
Cinescope/
├── 📁 api/                        # API модули
│   ├── api_manager.py            # Центральный менеджер API
│   ├── auth_api.py               # API аутентификации
│   ├── user_api.py               # API пользователей
│   ├── movies_api.py             # API фильмов
│   ├── genres_api.py             # API жанров
│   ├── reviews_api.py            # API отзывов
│   └── payment_api.py            # API платежей
├── 📁 custom_requester/          
│   └── custom_requester.py       # Кастомный HTTP клиент
├── 📁 entities/                  
│   └── user.py                   # Модели пользователей
├── 📁 models/                    
│   └── auth_model.py             # Модели аутентификации
├── 📁 resources/                 
│   ├── user_creds.py             # Учетные данные для тестов
│   └── test_card_data.py         # Тестовые данные карт для платежей
├── 📁 tests/                     
│   └── 📁 api/                   # API тесты
│       ├── test_auth_api.py      # Тесты аутентификации
│       ├── test_user_api.py      # Тесты пользователей
│       ├── test_movies_api.py    # Тесты фильмов
│       ├── test_genres_api.py    # Тесты жанров
│       ├── test_reviews_api.py   # Тесты отзывов
│       └── test_payment_api.py   # Тесты платежей
├── 📁 utils/                     
│   └── data_generator.py         # Генератор тестовых данных
├── conftest.py                   # Фикстуры pytest
├── constants.py                  # Глобальные константы
├── pytest.ini                   # Конфигурация pytest
└── requirements.txt              # Зависимости проекта
```

## ⚡ Быстрый старт

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd Cinescope
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Запуск тестов

#### Запуск всех тестов

```bash
.venv\Scripts\python.exe -m pytest
```

#### Запуск тестов конкретного модуля

```bash
.venv\Scripts\python.exe -m pytest tests/api/test_auth_api.py
.venv\Scripts\python.exe -m pytest tests/api/test_movies_api.py
.venv\Scripts\python.exe -m pytest tests/api/test_user_api.py
.venv\Scripts\python.exe -m pytest tests/api/test_payment_api.py
```

#### Запуск конкретного теста

```bash
.venv\Scripts\python.exe -m pytest tests/api/test_movies_api.py::TestMovieAPI::test_filter_movies_by_price
```

#### Запуск тестов с маркерами

```bash
.venv\Scripts\python.exe -m tests/api/test_movies_api.py -m marker_name
```

## 🧪 Архитектура тестирования

### API Модули

- **`AuthAPI`** - управление аутентификацией (логин, регистрация, токены)
- **`UserAPI`** - CRUD операции с пользователями
- **`MoviesAPI`** - работа с фильмами (создание, получение, фильтрация)
- **`GenresAPI`** - управление жанрами фильмов
- **`ReviewsAPI`** - система отзывов к фильмам
- **`PaymentAPI`** - создание платежей за фильмы

### Паттерны проектирования

- **Manager Pattern** - `api_manager.py` для централизованного управления API
- **Factory Pattern** - `data_generator.py` для генерации тестовых данных
- **Page Object Model** - для UI тестирования

### Роли и разрешения

- **PUBLIC** - публичный доступ (GET запросы)
- **USER** - базовые операции авторизованного пользователя
- **ADMIN** - административные функции
- **SUPER_ADMIN** - полный доступ ко всем операциям

## 💳 Платежная система

### Тестовые данные карт

Проект включает предопределенные тестовые данные карт в файле `resources/test_card_data.py`:

- Номер карты: `***` (Visa Test Card)
- Срок действия: `12/25`
- CVV: `***`
- Держатель карты: `Test User`

### Особенности тестирования платежей

- ✅ Позитивные сценарии: успешное создание платежа
- ❌ Негативные сценарии: невалидные карты, неавторизованный доступ, несуществующие фильмы
- 🔄 Автоматическое пропускание тестов при недоступности внешнего сервиса карт (503 ошибка)
- 📊 Динамическая генерация сумм платежей для каждого теста

## 📊 Отчеты и логирование

Тесты можно запускать с генерацией отчетов:

```bash
# HTML отчет
.venv\Scripts\python.exe -m pytest --html=reports/report.html

# JUnit XML отчет
.venv\Scripts\python.exe -m pytest --junitxml=reports/junit.xml

# Подробный вывод
.venv\Scripts\python.exe -m pytest -v

# Показать локальные переменные при ошибках
.venv\Scripts\python.exe -m pytest -l
```

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Соглашения о коде

- Названия тестов: `test_<действие>_<объект>_<условие>`
- Использование динамической генерации данных для предотвращения дублирования
- Маркировка негативных тестов с помощью `@pytest.mark.negative`
- Пропуск тестов при недоступности внешних сервисов с помощью `@pytest.mark.skip`
- Следование принципам SOLID и чистого кода
- Обязательное покрытие тестами новой функциональности

---

**Создано с ❤️ к автоматизации тестирования **