import pytest

from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User



@pytest.mark.api_senior
class TestCreateUser:
    @pytest.mark.parametrize(
        "create_user_request",
        [RandomModelGenerator.generate(CreateUserRequest)]
    )
    def test_create_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Ошибка: Созданного пользователя нет в БД'


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
    def test_create_user_invalid(self, username: str, password: str, api_manager: ApiManager, db_session: Session):
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'Ошибка: Пользователь создан'