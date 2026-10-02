import requests
import pytest

@pytest.mark.api_junior
class TestCreateUser:
    def test_create_user_valid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        assert login_admin_response.status_code == 200
        assert login_admin_response.json()["user"]["username"] == "admin"
        assert login_admin_response.json()["user"]["role"] == "ROLE_ADMIN"

        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Max03",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"

            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max03"
        assert create_user_response.json().get("role") == "ROLE_USER"


    @pytest.mark.parametrize(
        "username, password",
        [
            ("Лев", "Pas!sw0rd"), # Латиница
            ("Ma", "Pas!sw0rd"), # Не менее 3 букв (2 < 3)
            ("MaxMaxMaxMaxMaxX", "Pas!sw0rd"), # Максимум 15 букв (16 > 15)
            ("Max!", "Pas!sw0rd"),  # Запрещены спец. символы

            ("Max04", "Pas!sw0rд"),  # Латиница
            ("Max05", "Pas!sw0"),  # Не менее 8 символов (7 < 8)
            ("Max06", "pas!sw0rd"),  # Минимум 1 заглавная буква
            ("Max07", "PAS!SW0RD"),  # Минимум 1 маленькая буква
            ("Max08", "passsw0rd"),  # Минимум 1 спец. символ
            ("Max09", "Pas!swOrd")  # Минимум 1 спец. символ
        ]
        )
    def test_create_user_invalid(self, username, password):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token = login_admin_response.json().get("token")

        assert login_admin_response.status_code == 200
        assert login_admin_response.json()["user"]["username"] == "admin"
        assert login_admin_response.json()["user"]["role"] == "ROLE_ADMIN"


        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": username,
                "password": password,
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 400



