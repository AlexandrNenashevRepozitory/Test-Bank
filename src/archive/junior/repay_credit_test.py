import requests
import pytest

@pytest.mark.api_junior
class TestRepayCredit:
    def test_request_credit_valid(self):
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
                "username": "Max60",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"

            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json()["username"] == "Max60"
        assert create_user_response.json()["role"] == "ROLE_CREDIT_SECRET"


        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max60",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token = login_user_response.json().get("token")

        assert login_user_response.status_code == 200
        assert login_user_response.json()["user"]["username"] == "Max60"
        assert login_user_response.json()["user"]["role"] == "ROLE_CREDIT_SECRET"


        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        account_id = create_account_response.json().get("id")

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0


        request_credit_responce = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        credit_id = request_credit_responce.json().get("creditId")

        assert request_credit_responce.status_code == 201
        assert request_credit_responce.json().get("balance") >= 5000


        repay_credit_responce = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 5000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert repay_credit_responce.status_code == 200


    def test_request_credit_invalid(self):
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
                "username": "Max61",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"

            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json()["username"] == "Max61"
        assert create_user_response.json()["role"] == "ROLE_CREDIT_SECRET"


        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max61",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token = login_user_response.json().get("token")

        assert login_user_response.status_code == 200
        assert login_user_response.json()["user"]["username"] == "Max61"
        assert login_user_response.json()["user"]["role"] == "ROLE_CREDIT_SECRET"


        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        account_id = create_account_response.json().get("id")

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0


        request_credit_responce = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": account_id,
                "amount": 5000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        credit_id = request_credit_responce.json().get("creditId")

        assert request_credit_responce.status_code == 201
        assert request_credit_responce.json().get("balance") >= 5000


        repay_credit_responce = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 3000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )

        assert repay_credit_responce.status_code == 422


