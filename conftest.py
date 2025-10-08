# Импорт всех фикстур из отдельных модулей
# Это позволяет pytest автоматически обнаруживать все фикстуры

# Базовые фикстуры (сессии, API менеджер)
from fixtures.base_fixtures import *

# Фикстуры для аутентификации и пользователей
from fixtures.auth_fixtures import *

# Фикстуры для фильмов
from fixtures.movies_fixtures import *

# Фикстуры для жанров
from fixtures.genres_fixtures import *

# Фикстуры для отзывов
from fixtures.reviews_fixtures import *

# Фикстуры для платежей
from fixtures.payment_fixtures import *

# Фикстуры для БД тестов
from fixtures.db_fixtures import *
    