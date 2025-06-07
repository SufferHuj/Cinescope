Cinescope/ 
├── api/                                  # Пакет для работы с API
│   ├── init.py                           # Делает 'api' пакетом
│   ├── auth_api.py                       # Модуль для взаимодействия с API аутентификации (Auth API)
│   ├── user_api.py                       # Модуль для взаимодействия с API юзера (User API)
│   ├── api_manager.py                    # Центральный менеджер для взаимодействия с различными API
│   ├── movies_api.py                     # Модуль для взаимодействия с API фильмов (Movies API)
├── custom_requester/
│   └── custom_requester.py               # Кастомный реквестер для API запросов
├── utils/
│   └── data_generator.py                 # Генератор тестовых данных
├── enums/
│   └── hosts.py                          # Константы для URL и другие параметры
├── tests/
│   ├── api/                              # Тесты для API
│   │   ├── test_auth.py                  # Тесты для Auth API
│   │   └── test_movies_api.py            # Тесты для Movies API
│   ├── ui/                               # Тесты для UI
│   │   ├── test_login_page.py            # Тесты для страницы логина
│       └── test_registration_page.py     # Тесты для страницы регистрации
├── conftest.py                           # Фикстуры для Pytest
├── constants.py                          # Глобальные константы
├── pytest.ini                            # Конфигурация Pytest
├── requirements.txt                      # Зависимости проекта
├── entities/
│   ├── user.py                           # Модель юзеров
├── resources/
│   ├── user_creds.py                     # Креды пользователей
└── README.md