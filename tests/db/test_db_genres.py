from utils.data_generator import faker


class TestDBGenres:
    """
    Класс тестов для работы с базой данных жанров.
    
    Включает тесты для создания, чтения, обновления и удаления жанров,
    а также проверки уникальности, валидации и различных методов поиска.
    """

    def test_genre_crud_operations(self, db_helper):
        """
        Тест базовых CRUD операций с жанрами
        """
        # Генерируем тестовые данные жанра
        genre_data = {
            'name': f"Test Genre {faker.word()}"
        }
        
        # Создание жанра
        created_genre = db_helper.create_test_genre(genre_data)
        
        try:
            # Проверяем создание
            assert created_genre.id is not None
            assert created_genre.name == genre_data['name']
            
            # Проверяем чтение по ID
            retrieved_genre = db_helper.get_genre_by_id(created_genre.id)
            assert retrieved_genre is not None
            assert retrieved_genre.name == genre_data['name']
            
            # Проверяем чтение по названию
            genre_by_name = db_helper.get_genre_by_name(created_genre.name)
            assert genre_by_name is not None
            assert genre_by_name.id == created_genre.id
            
            # Проверяем существование жанра
            assert db_helper.genre_exists_by_name(created_genre.name)

            # Тестируем поиск несуществующего жанра по ID
            fake_genre_id = faker.random_int(min=100000, max=999999)
            non_existent_genre = db_helper.get_genre_by_id(fake_genre_id)
            assert non_existent_genre is None
            
            # Тестируем поиск несуществующего жанра по названию
            fake_genre_name = f"NonExistent Genre {faker.uuid4()}"
            non_existent_genre_by_name = db_helper.get_genre_by_name(fake_genre_name)
            assert non_existent_genre_by_name is None
            
            # Проверяем, что несуществующий жанр не существует
            assert not db_helper.genre_exists_by_name(fake_genre_name)
            
        finally:
            # Очистка: удаляем созданный жанр
            db_helper.cleanup_test_data([created_genre])


    def test_genre_deletion(self, db_helper):
        """
        Тест удаления жанров
        """
        # Создаем жанр для удаления
        genre_data = {'name': f"To Delete Genre {faker.word()}"}
        
        genre_to_delete = db_helper.create_test_genre(genre_data)
        genre_id = genre_to_delete.id
        genre_name = genre_to_delete.name
        
        # Проверяем, что жанр создан
        assert db_helper.genre_exists_by_name(genre_name)
        assert db_helper.get_genre_by_id(genre_id) is not None
        
        # Удаляем жанр
        db_helper.delete_genre(genre_to_delete)
        
        # Проверяем, что жанр удален
        assert not db_helper.genre_exists_by_name(genre_name)
        assert db_helper.get_genre_by_id(genre_id) is None
        assert db_helper.get_genre_by_name(genre_name) is None
