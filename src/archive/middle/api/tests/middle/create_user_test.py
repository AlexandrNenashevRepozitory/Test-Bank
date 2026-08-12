import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.responce_specs import ResponseSpecs


@pytest.mark.api_middle
class TestCreateUser:
    def test_create_user_valid(self):
        create_user_request = CreateUserRequest(username="Max100", password="Pas!sw0rd", role="ROLE_USER")

        response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)


        assert create_user_request.username == response.username
        assert create_user_request.role == response.role


    @pytest.mark.parametrize(
        "username, password",
        [
            ("Лев", "Pas!sw0rd"), # Латиница
            ("Ma", "Pas!sw0rd"), # Не менее 3 букв (2 < 3)
            ("MaxMaxMaxMaxMaxX", "Pas!sw0rd"), # Максимум 15 букв (16 > 15)
            ("Max!", "Pas!sw0rd"),  # Запрещены спец. символы

            ("Max104", "Pas!sw0rд"),  # Латиница
            ("Max105", "Pas!sw0"),  # Не менее 8 символов (7 < 8)
            ("Max106", "pas!sw0rd"),  # Минимум 1 заглавная буква
            ("Max107", "PAS!SW0RD"),  # Минимум 1 маленькая буква
            ("Max108", "passsw0rd"),  # Минимум 1 спец. символ
            ("Max109", "Pas!swOrd")  # Минимум 1 спец. символ
        ]
        )
    def test_create_user_invalid(self, username, password):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)