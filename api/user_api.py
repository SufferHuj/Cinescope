from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL


class UserAPI(CustomRequester):
    """ Класс для работы с API пользователей """

    def __init__(self, session):

        super().__init__(session=session, base_url=BASE_URL)

    def get_user(self, user_id, expected_status=200):
        """ Получение информации о пользователе """

        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def get_users(self, page_size=None, page=None, roles=None, created_at=None, expected_status=200):
        """ Получение списка пользователей """
        
        params = {}
        if page_size is not None:
            params['pageSize'] = page_size
        if page is not None:
            params['page'] = page
        if roles is not None:
            params['roles'] = roles
        if created_at is not None:
            params['createdAt'] = created_at

        return self.send_request(
            method="GET",
            endpoint="/user",
            params=params,
            expected_status=expected_status
        )

    def create_user(self, user_data, expected_status=201):
        """ Создание пользователя """

        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )

    def patch_user(self, user_id, user_data, expected_status=200):
        """ Обновление пользователя """

        return self.send_request(
            method="PATCH",
            endpoint=f"/user/{user_id}",
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id, expected_status=200):
        """ Удаление пользователя """

        # Сохраняем текущие Cookie
        original_cookies = self.session.cookies.copy()
        
        # Очищаем Cookie для DELETE запроса
        self.session.cookies.clear()
        
        try:
            response = self.send_request(
                method="DELETE",
                endpoint=f"/user/{user_id}",
                expected_status=expected_status
            )
        finally:
            # Восстанавливаем Cookie после запроса
            self.session.cookies.update(original_cookies)
            
        return response

    def clean_up_user(self, user_id):
        """ Метод для удаления пользователя после теста """

        try:
            self.delete_user(user_id=user_id, expected_status=200)

        except ValueError as error:

            if "Unexpected status code: 404" in str(error):
                print(f"User with ID {user_id} not found during cleanup (possibly already deleted). "
                      f"Skipping.")
            else:
                print(f"Error during user cleanup for ID {user_id}: {error}")
                raise  # Перевыбрасываем другие неожиданные ошибки
