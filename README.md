Cinescope/ #Это название проекта
├── custom_requester/
│   └── custom_requester.py              # Кастомный реквестер для API запросов
├── utils/
│   └── data_generator.py                  # Генератор тестовых данных
├── enums/
│   └── hosts.py                                  # Константы для URL и другие параметры
├── tests/
│   ├── api/                                         # Тесты для API
│   │   ├── test_auth.py                       # Тесты для Auth API
│   │   └── test_other_api.py               # Другие API тесты
│   ├── ui/                                           # Тесты для UI
│   │   ├── test_login_page.py            # Тесты для страницы логина
│   │   └── test_registration_page.py # Тесты для страницы регистрации
│   └── init.py                                    # Пустой файл для обозначения пакета
├── conftest.py                                  # Фикстуры для Pytest
├── constants.py                               # Глобальные константы
├── pytest.ini                                    # Конфигурация Pytest
├── requirements.txt                        # Зависимости проекта
└── README.md