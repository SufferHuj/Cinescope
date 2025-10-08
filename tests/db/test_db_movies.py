from utils.data_generator import faker


class TestDBMovies:
    """ Класс тестов для работы с базой данных фильмов """

    def test_db_movie_requests(self, db_helper, movie_test_data):
        """ Тест базовых операций с фильмами через DBHelper """
        
        # Создаем тестовый фильм
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        try:
            # Проверяем, что фильм создан
            assert created_movie.id is not None
            assert created_movie.name == movie_test_data['name']
            
            # Проверяем получение фильма по ID
            retrieved_movie = db_helper.movies.get_movie_by_id(created_movie.id)
            assert retrieved_movie is not None
            
        finally:
            # Очищаем тестовые данные (пользователь очистится автоматически через фикстуру)
            db_helper.cleanup_test_data([created_movie])

    def test_movie_crud_operations(self, db_helper, movie_test_data):
        """ Тест CRUD операций с фильмами """

        # Создание фильма
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        try:
            # Проверяем чтение по ID
            retrieved_movie = db_helper.movies.get_movie_by_id(created_movie.id)
            assert retrieved_movie is not None
            assert retrieved_movie.name == movie_test_data['name']
            
            # Проверяем чтение по названию
            movie_by_name = db_helper.movies.get_movie_by_name(created_movie.name)
            assert movie_by_name is not None
            assert movie_by_name.id == created_movie.id
            
            # Проверяем существование фильма
            assert db_helper.movies.movie_exists_by_name(created_movie.name)
            
        finally:
            # Удаляем тестовый фильм
            db_helper.cleanup_test_data([created_movie])

    def test_movie_filtering_methods(self, db_helper, movie_test_data):
        """ Тест методов фильтрации фильмов """

        # Создаем несколько фильмов с разными параметрами
        movie_data_1 = movie_test_data.copy()
        movie_data_1['name'] = f"Фильм 1 - {faker.catch_phrase()}"
        movie_data_1['genre_id'] = 1
        movie_data_1['price'] = 500
        
        movie_data_2 = movie_test_data.copy()
        movie_data_2['name'] = f"Фильм 2 - {faker.catch_phrase()}"
        movie_data_2['genre_id'] = 2
        movie_data_2['price'] = 601
        
        movie_data_3 = movie_test_data.copy()
        movie_data_3['name'] = f"Фильм 3 - {faker.catch_phrase()}"
        movie_data_3['genre_id'] = 1
        movie_data_3['price'] = 299
        
        movie1 = db_helper.movies.create_test_movie(movie_data_1)
        movie2 = db_helper.movies.create_test_movie(movie_data_2)
        movie3 = db_helper.movies.create_test_movie(movie_data_3)

        try:
            # Тестируем фильтрацию по жанру
            genre_1_movies = db_helper.movies.get_movies_by_genre(1)
            genre_1_ids = [movie.id for movie in genre_1_movies]
            assert movie1.id in genre_1_ids
            assert movie3.id in genre_1_ids
            assert movie2.id not in genre_1_ids

            # Тестируем фильтрацию по диапазону цен
            price_range_movies = db_helper.movies.get_movies_by_price_range(300, 600)
            price_range_ids = [movie.id for movie in price_range_movies]
            assert movie1.id in price_range_ids
            assert movie2.id not in price_range_ids
            assert movie3.id not in price_range_ids

        finally:
            # Очищаем тестовые данные
            db_helper.cleanup_test_data([movie1, movie2, movie3])

    def test_movie_count_methods(self, db_helper, movie_test_data):
        """ Тест методов подсчета количества записей """

        # Получаем изначальное количество фильмов ДО создания тестового фильма
        initial_movies_count = db_helper.get_total_movies_count()
        
        # Создаем тестовый фильм
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        try:
            # Проверяем, что количество увеличилось на 1 после создания фильма
            current_movies_count = db_helper.get_total_movies_count()
            assert current_movies_count == initial_movies_count + 1, \
                f"Ожидалось {initial_movies_count + 1} фильмов, получено {current_movies_count}"
            
        finally:
            # Очищаем тестовые данные
            db_helper.cleanup_test_data([created_movie])

    def test_movie_existence_check(self, db_helper, movie_test_data):
        """ Тест проверки существования фильма """

        # Проверяем, что несуществующий фильм не найден
        fake_movie_name = f"Несуществующий фильм {faker.uuid4()}"
        assert not db_helper.movies.movie_exists_by_name(fake_movie_name)
        
        # Создаем фильм и проверяем, что он найден
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        try:
            assert db_helper.movies.movie_exists_by_name(created_movie.name)
        finally:
            # Очищаем тестовые данные
            db_helper.movies.delete_movie(created_movie)
            
        # Проверяем, что после удаления фильм не найден
        assert not db_helper.movies.movie_exists_by_name(created_movie.name)
