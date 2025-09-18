"""
Модуль для работы с базой данных PostgreSQL.
Содержит настройки подключения и создание сессий для работы с БД.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys
import os

# Добавляем родительскую директорию в путь для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resources.db_creds import MoviesDbCreds

USERNAME = MoviesDbCreds.USERNAME
PASSWORD = MoviesDbCreds.PASSWORD
HOST = MoviesDbCreds.HOST
PORT = MoviesDbCreds.PORT
DATABASE_NAME = MoviesDbCreds.DATABASE_NAME

# Движок для подключения к базе данных PostgreSQL
engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=True  # Установить True для отладки SQL запросов
)

# Создаем фабрику сессий для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """
    Создает новую сессию БД.
    :return: Объект сессии SQLAlchemy для работы с базой данных.
    """
    return SessionLocal()

if __name__ == "__main__":
    # Тестируем подключение к базе данных
    try:
        session = get_db_session()
        print("[OK] Database connection successful!")
        print(f"[INFO] Connection: {HOST}:{PORT}/{DATABASE_NAME}")
        print(f"[INFO] User: {USERNAME}")
        
        # Тестовый запрос для проверки соединения
        result = session.execute(text("SELECT 1"))
        print("[TEST] Test query executed successfully")
        
        session.close()
        print("[INFO] Session closed")
        
    except Exception as e:
        print(f"[ERROR] Database connection error: {e}")
