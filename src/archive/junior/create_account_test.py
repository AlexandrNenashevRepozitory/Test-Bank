import requests
import pytest

@pytest.mark.api_junior
class TestCreateAccount:
    def test_create_account(self):
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
                "username": "Max22",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"

            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max22"
        assert create_user_response.json().get("role") == "ROLE_USER"


        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max22",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token = login_user_response.json().get("token")

        assert login_user_response.status_code == 200
        assert login_user_response.json()["user"]["username"] == "Max22"
        assert login_user_response.json()["user"]["role"] == "ROLE_USER"


        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
