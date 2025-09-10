import pytest


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        """
        Успешное создание пользователя
        """

        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True

    def test_patch_update_user(self, super_admin, creation_user_data):
        """
        Обновление данных пользователя через Patch
        """

        params = {
            "roles": ["ADMIN"]
        }
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        updated_patch_response = super_admin.api.user_api.patch_user(created_user_response["id"],
                                                                     user_data=params).json()

        assert updated_patch_response.get("roles", []) == ["ADMIN"]

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """
        Успешное получение данных о пользователе
        """

        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    def test_get_users_success(self, super_admin):
        """
        Успешное получение списка пользователей
        """

        response = super_admin.api.user_api.get_users().json()

        assert 'users' in response, "В ответе должен быть ключ 'users'"
        assert 'count' in response, "В ответе должен быть ключ 'count'"
        assert 'page' in response, "В ответе должен быть ключ 'page'"
        assert 'pageSize' in response, "В ответе должен быть ключ 'pageSize'"

    # НЕГАТИВНЫЙ ТЕСТ
    @pytest.mark.negative
    def test_get_user_by_id_common_user(self, common_user):
        """
        Невалидное получение данных о пользователе (с ролью user недоступно)
        """

        response = common_user.api.user_api.get_user(common_user.email, expected_status=403)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data.get("error") == "Forbidden"
        assert response_data.get("message") == "Forbidden resource"

    @pytest.mark.negative
    def test_get_users_invalid_params(self, super_admin):
        """
        Невалидные параметры при получении списка пользователей
        """

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

        try:
            error_data = response_invalid_pagesize.json()
            assert "error" in error_data or "message" in error_data, "Ответ должен содержать информацию об ошибке"
        except ValueError:
            # Если ответ не в формате JSON, это тоже ошибка
            assert False, "Ответ с ошибкой должен быть в формате JSON"
