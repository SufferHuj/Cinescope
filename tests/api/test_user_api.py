import pytest
from models.user_model import CreateUserResponse, GetUserResponse, GetUsersResponse, UpdateUserResponse
from models.auth_model import ErrorResponse
from utils.data_generator import DataGenerator


class TestUser:
    """ Класс тестов для API пользователей """

    def test_create_user(self, super_admin, creation_user_data):
        """ Успешное создание пользователя """

        response = super_admin.api.user_api.create_user(creation_user_data)
        response_data = CreateUserResponse(**response.json())

        assert response_data.id and response_data.id != '', "ID должен быть не пустым"
        assert response_data.email == creation_user_data['email'], "Email не совпадает"
        assert response_data.fullName == creation_user_data['fullName'], "Имя не совпадает"
        assert response_data.roles == creation_user_data['roles'], "Роли не совпадают"
        assert response_data.verified is True, "Пользователь должен быть верифицирован"

    def test_patch_update_user(self, super_admin, creation_user_data):
        """ Обновление данных пользователя через Patch """

        params = {
            "roles": ["ADMIN"]
        }
        created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        created_user_data = CreateUserResponse(**created_user_response.json())
        
        updated_patch_response = super_admin.api.user_api.patch_user(created_user_data.id, user_data=params)
        updated_patch_data = UpdateUserResponse(**updated_patch_response.json())

        assert updated_patch_data.roles == ["ADMIN"], "Роли не обновились корректно"

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """ Получение пользователя по локатору """

        created_user_response = super_admin.api.user_api.create_user(creation_user_data)
        created_user_data = CreateUserResponse(**created_user_response.json())
        
        get_user_response = super_admin.api.user_api.get_user(created_user_data.id)
        get_user_data = GetUserResponse(**get_user_response.json())

        assert get_user_data.id == created_user_data.id, "ID не совпадает"
        assert get_user_data.email == created_user_data.email, "Email не совпадает"
        assert get_user_data.fullName == created_user_data.fullName, "Имя не совпадает"
        assert get_user_data.roles == created_user_data.roles, "Роли не совпадают"
        assert get_user_data.verified == created_user_data.verified, "Статус верификации не совпадает"

    def test_get_users_success(self, super_admin):
        """ Успешное получение списка пользователей """

        response = super_admin.api.user_api.get_users()
        users_data = GetUsersResponse(**response.json())

        assert isinstance(users_data.users, list), "Ответ должен быть списком"
        assert len(users_data.users) > 0, "Список пользователей не должен быть пустым"

        # Проверяем структуру первого пользователя
        first_user = users_data.users[0]
        assert first_user.id, "У пользователя должен быть ID"
        assert first_user.email, "У пользователя должен быть email"
        assert first_user.fullName, "У пользователя должно быть полное имя"
        assert first_user.roles, "У пользователя должны быть роли"

    def test_get_users_pagination(self, super_admin):
        """ Проверка пагинации при получении списка пользователей """

        response = super_admin.api.user_api.get_users()
        users_data = GetUsersResponse(**response.json())

        assert users_data.users is not None, "В ответе должен быть список пользователей"
        assert users_data.count is not None, "В ответе должен быть ключ 'count'"
        assert users_data.page is not None, "В ответе должен быть ключ 'page'"
        assert users_data.pageSize is not None, "В ответе должен быть ключ 'pageSize'"

    # НЕГАТИВНЫЙ ТЕСТ
    @pytest.mark.negative
    def test_get_user_by_id_common_user(self, common_user):
        """ Невалидное получение данных о пользователе (с ролью user недоступно) """

        response = common_user.api.user_api.get_user(common_user.email, expected_status=403)
        
        assert response.status_code == 403
        
        error_data = ErrorResponse(**response.json())
        assert error_data.error == "Forbidden", "Ошибка должна быть 'Forbidden'"
        if error_data.message:
            assert error_data.message == "Forbidden resource", "Сообщение должно быть 'Forbidden resource'"

    @pytest.mark.negative
    def test_get_users_invalid_params(self, super_admin):
        """ Невалидные параметры при получении списка пользователей """

        # Отправляем запрос с невалидным значением pageSize
        response_invalid_pagesize = super_admin.api.user_api.get_users(page_size=-1, expected_status=400)
        assert response_invalid_pagesize.status_code == 400

        # Проверяем невалидное значение page
        response_invalid_page = super_admin.api.user_api.get_users(page=-1, expected_status=400)
        assert response_invalid_page.status_code == 400

        # Проверяем невалидное значение roles (несуществующая роль)
        response_invalid_roles = super_admin.api.user_api.get_users(roles=["INVALID_ROLE"], expected_status=[400, 500])
        assert response_invalid_roles.status_code in [400, 500]

        # Проверяем невалидное значение createdAt
        response_invalid_created_at = super_admin.api.user_api.get_users(created_at="invalid_sort",
                                                                         expected_status=[400, 500])
        assert response_invalid_created_at.status_code in [400, 500]

        # Проверяем, что все ответы содержат валидные сообщения об ошибках
        responses_to_check = [response_invalid_pagesize, response_invalid_page, response_invalid_roles, response_invalid_created_at]
        
        for response in responses_to_check:
            try:
                error_data = ErrorResponse(**response.json())
                assert error_data.error or error_data.message or error_data.statusCode, "Ответ должен содержать информацию об ошибке"
            except (ValueError, TypeError):
                # Если ответ не в формате JSON или не может быть распарсен, это тоже ошибка
                assert False, f"Ответ с ошибкой должен быть в формате JSON. Статус: {response.status_code}, Содержимое: {response.text}"

    @pytest.mark.negative
    def test_get_user_not_found(self, super_admin):
        """ Получение несуществующего пользователя """
        
        non_existent_id = DataGenerator.generation_random_uuid()

        response = super_admin.api.user_api.create_user(non_existent_id, expected_status=400)
        assert response.status_code == 400

        error_data = ErrorResponse(**response.json())
        assert error_data.error, "Должно быть сообщение об ошибке"
