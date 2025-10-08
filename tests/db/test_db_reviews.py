from utils.data_generator import DataGenerator, faker


class TestDBReviews:
    """ Тесты для работы с базой данных отзывов """

    def test_review_crud_operations(self, db_helper, created_test_user, movie_test_data, review_test_data):
        """ Тест базовых CRUD операций с отзывами """
        # Создаем тестовый фильм
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        # Генерируем тестовые данные отзыва с существующими ID
        review_data = review_test_data.copy()
        review_data.update({
            'movie_id': created_movie.id,
            'user_id': created_test_user.id
        })
        
        # Создание отзыва
        created_review = db_helper.reviews.create_test_review(review_data)
        
        try:
            # Проверяем чтение по составному ключу
            retrieved_review = db_helper.reviews.get_review_by_ids(
                created_review.movie_id, 
                created_review.user_id
            )
            assert retrieved_review is not None
            assert retrieved_review.text == review_data['text']
            assert retrieved_review.rating == review_data['rating']
            
            # Проверяем существование отзыва
            assert db_helper.reviews.review_exists_by_ids(
                created_review.movie_id, 
                created_review.user_id
            )
            
            # Тестируем поиск несуществующего отзыва
            fake_user_data = DataGenerator.generate_user_data()
            fake_movie_id = faker.random_int(min=99999, max=999999)
            non_existent_review = db_helper.reviews.get_review_by_ids(fake_movie_id, fake_user_data['id'])
            assert non_existent_review is None
            
            # Проверяем несуществование отзыва
            assert not db_helper.reviews.review_exists_by_ids(fake_movie_id, fake_user_data['id'])
            
        finally:
            # Удаляем тестовые данные
            db_helper.cleanup_test_data([created_review, created_movie])

    def test_review_filtering_by_movie(self, db_helper, movie_test_data, review_test_data):
        """ Тест фильтрации отзывов по фильму """
        # Создаем тестовый фильм
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        # Создаем несколько отзывов для одного фильма
        created_reviews = []
        created_users = []
        
        for i in range(2):
            # Создаем тестового пользователя для каждого отзыва
            user_data = DataGenerator.generate_user_data()
            test_user = db_helper.users.create_test_user(user_data)
            created_users.append(test_user)
            
            review_data = review_test_data.copy()
            review_data.update({
                'movie_id': created_movie.id,
                'user_id': test_user.id
            })
            created_reviews.append(db_helper.reviews.create_test_review(review_data))
        
        try:
            # Получаем все отзывы для фильма
            movie_reviews = db_helper.reviews.get_reviews_by_movie_id(created_movie.id)
            
            # Проверяем, что найдены все созданные отзывы
            assert len(movie_reviews) >= 2
            
            # Проверяем, что все отзывы принадлежат нужному фильму
            for review in movie_reviews:
                assert review.movie_id == created_movie.id
                
        finally:
            # Очистка тестовых данных
            db_helper.cleanup_test_data(created_reviews + created_users + [created_movie])


    def test_review_update_operations(self, db_helper, created_test_user, movie_test_data, review_test_data):
        """ Тест операций обновления отзывов """
        # Создаем тестовый фильм
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        # Создаем отзыв для обновления
        review_data = review_test_data.copy()
        review_data.update({
            'movie_id': created_movie.id,
            'user_id': created_test_user.id,
            'rating': 3  # Фиксированный рейтинг для теста обновления
        })
        
        created_review = db_helper.reviews.create_test_review(review_data)
        
        try:
            # Тестируем обновление рейтинга
            new_rating = 5
            db_helper.reviews.update_review_rating(
                created_review.movie_id, 
                created_review.user_id, 
                new_rating
            )
            
            # Получаем обновленный отзыв для проверки
            updated_review = db_helper.reviews.get_review_by_ids(
                created_review.movie_id, 
                created_review.user_id
            )
            assert updated_review.rating == new_rating
            
            # Тестируем обновление текста
            new_text = "Обновленный текст отзыва"
            db_helper.reviews.update_review_text(
                created_review.movie_id, 
                created_review.user_id, 
                new_text
            )
            
            # Получаем обновленный отзыв для проверки
            updated_review = db_helper.reviews.get_review_by_ids(
                created_review.movie_id, 
                created_review.user_id
            )
            assert updated_review.text == new_text
            
            # Тестируем скрытие отзыва
            db_helper.reviews.hide_review(
                created_review.movie_id, 
                created_review.user_id
            )
            
            # Получаем обновленный отзыв для проверки
            hidden_review = db_helper.reviews.get_review_by_ids(
                created_review.movie_id, 
                created_review.user_id
            )
            assert hidden_review.hidden is True
            
            # Тестируем показ отзыва
            db_helper.reviews.show_review(
                created_review.movie_id, 
                created_review.user_id
            )
            
            # Получаем обновленный отзыв для проверки
            shown_review = db_helper.reviews.get_review_by_ids(
                created_review.movie_id, 
                created_review.user_id
            )
            assert shown_review.hidden is False
            
        finally:
            # Очистка тестовых данных
            db_helper.cleanup_test_data([created_review, created_movie])

    def test_review_deletion(self, db_helper, created_test_user, movie_test_data, review_test_data):
        """ Тест удаления отзывов """
        # Создаем тестовый фильм
        created_movie = db_helper.movies.create_test_movie(movie_test_data)
        
        # Создаем отзыв для удаления
        review_data = review_test_data.copy()
        review_data.update({
            'movie_id': created_movie.id,
            'user_id': created_test_user.id
        })
        
        created_review = db_helper.reviews.create_test_review(review_data)
        
        try:
            # Удаляем отзыв по объекту
            db_helper.reviews.delete_review(created_review)
            
            # Проверяем, что отзыв удален
            assert not db_helper.reviews.review_exists_by_ids(
                created_review.movie_id, 
                created_review.user_id
            )
            
            # Создаем новый отзыв для тестирования удаления по ID
            new_review = db_helper.reviews.create_test_review(review_data)
            
            # Удаляем отзыв по ID
            db_helper.reviews.delete_review_by_ids(
                new_review.movie_id, 
                new_review.user_id
            )
            
            # Проверяем, что отзыв удален
            assert not db_helper.reviews.review_exists_by_ids(
                new_review.movie_id, 
                new_review.user_id
            )
            
        finally:
            # Очистка тестовых данных (фильм)
            db_helper.cleanup_test_data([created_movie])
