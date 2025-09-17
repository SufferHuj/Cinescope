import psycopg2
from psycopg2 import sql
from resources.db_creds import DatabaseCreds


def connect_to_database():
    """
    Подключается к базе данных db_movies и выводит информацию о PostgreSQL сервере
    Returns:
        psycopg2.connection: Объект подключения к базе данных или None в случае ошибки
    """
    
    try:
        # Создание подключения к базе данных
        connection = psycopg2.connect(
            host=DatabaseCreds.HOST,
            port=DatabaseCreds.PORT,
            database=DatabaseCreds.NAME,
            user=DatabaseCreds.USER,
            password=DatabaseCreds.PASSWORD
        )
        
        # Создание курсора для выполнения SQL запросов
        cursor = connection.cursor()
        
        print("Successfully connected to database!")
        print("=" * 50)
        
        # Получение информации о версии PostgreSQL
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"PostgreSQL Version: {version[0]}")
        
        # Получение информации о текущей базе данных
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()
        print(f"Current Database: {current_db[0]}")
        
        # Получение информации о текущем пользователе
        cursor.execute("SELECT current_user;")
        current_user = cursor.fetchone()
        print(f"Current User: {current_user[0]}")
        
        # Получение информации о хосте и порте сервера
        cursor.execute("SELECT inet_server_addr(), inet_server_port();")
        server_info = cursor.fetchone()
        print(f"Server Address: {server_info[0]}")
        print(f"Server Port: {server_info[1]}")
        
        # Получение списка всех таблиц в базе данных
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(f"\nTables in database ({len(tables)} total):")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Получение информации о размере базы данных
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database()));
        """)
        db_size = cursor.fetchone()
        print(f"\nDatabase Size: {db_size[0]}")
        
        print("=" * 50)
        
        return connection
        
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        return None
    
    finally:
        # Закрытие курсора и соединения с базой данных
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection:
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    connect_to_database()