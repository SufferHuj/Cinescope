import json
import logging
import os
from constants import BASE_URL, HEADERS, RED, GREEN, PURPLE, RESET
from pydantic import BaseModel


class CustomRequester:
    """
    Инициализация кастомного реквестера
    :param session: Объект requests.Session
    :param base_url: Базовый URL API
    :param default_headers: Заголовки, которые будут использоваться по умолчанию для всех запросов
    """

    def __init__(self, session, base_url=BASE_URL, default_headers=None):
        self.session = session
        self.base_url = base_url
        self.base_headers = HEADERS.copy()
        if default_headers:
            self.base_headers.update(default_headers)
        
        # Обновляем заголовки сессии
        self.session.headers = self.base_headers.copy()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(self, method, endpoint, data=None, params=None, headers=None, expected_status=200,
                     need_logging=True):
        """
        Универсальный метод для отправки запросов.
        :param method: HTTP метод (GET, POST, PUT, DELETE и т.д.).
        :param endpoint: эндпоинт (например, "/login").
        :param data: Тело запроса (JSON-данные).
        :param params: Параметры запроса (для GET-запросов).
        :param headers: Дополнительные заголовки для данного конкретного запроса.
        :param expected_status: Ожидаемый статус-код (по умолчанию 200).
        :param need_logging: Флаг для логирования (по умолчанию True).
        :return: Объект ответа requests.Response.
        """

        url = f"{self.base_url}{endpoint}"

        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
            
        # Проверяем, является ли data моделью Pydantic
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))
            
        response = self.session.request(method, url, json=data, params=params, headers=request_headers)

        if need_logging:
            self.log_request_and_response(response)

        if isinstance(expected_status, (list, tuple)):
            if response.status_code not in expected_status:
                raise ValueError(
                    f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
                )
        elif isinstance(expected_status, int):
            if response.status_code != expected_status:
                raise ValueError(f"Unexpected status code: {response.status_code}. Expected: {expected_status}")

        return response

    def _update_session_headers(self, **kwargs):
        """
        Обновление заголовков сессии.
        :param session: Объект requests.Session, предоставленный API-классом.
        :param kwargs: Дополнительные заголовки.
        """
        self.session.headers.update(kwargs)  # Обновляем базовые заголовки

    def log_request_and_response(self, response):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\ ".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            
            # Получаем информацию о тесте
            test_info = os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')
            full_test_name = f"pytest {test_info}"
            
            # Определяем цвет теста на основе статуса ответа
            # Если статус код указывает на ошибку (4xx, 5xx), используем красный цвет
            if response.status_code >= 400:
                test_color = RED
            else:
                test_color = GREEN

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body_text = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body_text = request.body
                else:
                    body_text = str(request.body)
                
                # Пытаемся распарсить JSON для корректного отображения кириллицы
                try:
                    body_json = json.loads(body_text)
                    body_text = json.dumps(body_json, ensure_ascii=False)
                except (ValueError, json.JSONDecodeError):
                    # Если не JSON, оставляем как есть
                    pass
                
                body = f"-d '{body_text}' \n" if body_text != '{}' else ''

            # Логируем request
            self.logger.info(f"\n{'=' * 35} {PURPLE}REQUEST{RESET} {'=' * 35}")    
            self.logger.info(
                f"{test_color}{full_test_name}{RESET}\n"
                f"curl -X {PURPLE}{request.method} {request.url}{RESET}  \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            
            # Форматируем данные для лучшей читаемости
            try:
                if response.content:
                    response_json = response.json()
                    # Используем ensure_ascii=False для корректного отображения Unicode символов
                    response_data = json.dumps(response_json, indent=4, ensure_ascii=False)
                else:
                    response_data = response.text
            except (ValueError, json.JSONDecodeError):
                response_data = response.text
            
            # Логируем response для всех запросов
            self.logger.info(f"\n{'=' * 34} {PURPLE}RESPONSE{RESET} {'=' * 35}")
            if is_success:
                self.logger.info(f"\tSTATUS_CODE: {GREEN}{response_status}{RESET}"
                               f"\nDATA: {response_data}{RESET}")
            else:
                self.logger.info(f"\tSTATUS_CODE: {RED}{response_status}{RESET}"
                               f"\nDATA: {RED}{response_data}{RESET}")
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")
