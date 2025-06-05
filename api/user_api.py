from custom_requester.custom_requester import CustomRequester

class UserAPI(CustomRequester):

    """
    Класс для работы с API пользователей
    """

    # ИЗМЕНЕНО: Конструктор теперь принимает session и base_url
    def __init__(self, session, base_url):
        # ИЗМЕНЕНО: Передаем оба аргумента в super().__init__()
        super().__init__(session=session, base_url=base_url)
        # self.session = session # Эту строку можно удалить, так как CustomRequester уже сохраняет session

    def get_user_info(self, user_id, expected_status = 200):

        """
        Получение информации о пользователе
        :param expected_status: Ожидаемый статус-код.
        :param user_id: ID пользователя.
        """
        return self.send_request(
            method= "GET",
            endpoint= f"/users/{user_id}",
            expected_status= expected_status
        )

    def delete_user(self, user_id, expected_status = 204):

        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f"/users/{user_id}",
            expected_status=expected_status
        )

    def clean_up_user(self, user_id):
        """
        Метод для очистки (удаления) пользователя после теста.
        Использует метод delete_user.
        :param user_id: ID пользователя, которого нужно удалить.
        """
        # Мы ожидаем статус 204 при успешном удалении.
        # Этот метод не должен выбрасывать ошибку, если пользователь уже не существует (например, 404),
        # так как это "очистка". Можно обработать это условие.
        try:
            self.delete_user(user_id=user_id, expected_status=204)

        except ValueError as error:
            # Если статус не 204, но это, например, 404 (Not Found),
            # это может означать, что пользователь уже был удален, и это приемлемо для очистки.
            # Если это другая ошибка, например, 500, то можно ее перевыбросить или залогировать.
            if "Unexpected status code: 404" in str(error):
                print(f"Пользователь с идентификатором {user_id} не найден во время очистки (возможно, он уже удален). "
                      f"Пропускаем.")
            else:
                print(f"Ошибка при очистке пользователя для идентификатора {user_id}: {error}")
                raise # Перевыбрасываем другие неожиданные ошибки