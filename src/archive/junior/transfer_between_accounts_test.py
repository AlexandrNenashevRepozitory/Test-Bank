import requests
import pytest

@pytest.mark.api_junior
class TestTransferBetweenAccounts:
    def test_transfer_between_accounts_valid(self):
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


        create_from_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Max40",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"

            }
        )

        assert create_from_user_response.status_code == 200
        assert create_from_user_response.json()["username"] == "Max40"
        assert create_from_user_response.json()["role"] == "ROLE_USER"


        login_from_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max40",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token_from_user = login_from_user_response.json().get("token")

        assert login_from_user_response.status_code == 200
        assert login_from_user_response.json()["user"]["username"] == "Max40"
        assert login_from_user_response.json()["user"]["role"] == "ROLE_USER"


        create_from_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_from_user}"
            }
        )

        from_account_id = create_from_account_response.json().get("id")

        assert create_from_account_response.status_code == 201
        assert create_from_account_response.json().get("balance") == 0


        replenishment_from_account_responce = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": from_account_id,
                "amount": 1500.5
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_from_user}",
                "Content-Type": "application/json"
            }
        )

        assert replenishment_from_account_responce.status_code == 200
        assert replenishment_from_account_responce.json().get("balance") > 0


        create_to_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Max41",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"
            }
        )

        assert create_to_user_response.status_code == 200
        assert create_to_user_response.json()["username"] == "Max41"
        assert create_to_user_response.json()["role"] == "ROLE_USER"


        login_to_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max41",
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token_to_user = login_to_user_response.json().get("token")

        assert login_to_user_response.status_code == 200
        assert login_to_user_response.json()["user"]["username"] == "Max41"
        assert login_to_user_response.json()["user"]["role"] == "ROLE_USER"


        create_to_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_to_user}"
            }
        )

        to_account_id = create_to_account_response.json().get("id")

        assert create_to_account_response.status_code == 201
        assert create_to_account_response.json().get("balance") == 0


        transfer_account_responce = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": from_account_id,
                "toAccountId": to_account_id,
                "amount": 500.75
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_from_user}",
                "Content-Type": "application/json",
            }
        )

        assert transfer_account_responce.status_code == 200
        assert transfer_account_responce.json().get("fromAccountIdBalance") < 1000
        assert transfer_account_responce.json().get("fromAccountId") == from_account_id
        assert transfer_account_responce.json().get("toAccountId") == to_account_id



    @pytest.mark.parametrize(
        "from_username, to_username, amount",
        [
            ("Max43", "Max45", "499"),
            ("Max44", "Max46", "10001")
        ]
        )
    def test_transfer_between_accounts_invalid(self, from_username, to_username, amount):
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


        create_from_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": from_username,
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"

            }
        )

        assert create_from_user_response.status_code == 200
        assert create_from_user_response.json()["username"] == from_username
        assert create_from_user_response.json()["role"] == "ROLE_USER"


        login_from_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": from_username,
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token_from_user = login_from_user_response.json().get("token")

        assert login_from_user_response.status_code == 200
        assert login_from_user_response.json()["user"]["username"] == from_username
        assert login_from_user_response.json()["user"]["role"] == "ROLE_USER"


        create_from_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_from_user}"
            }
        )

        from_account_id = create_from_account_response.json().get("id")

        assert create_from_account_response.status_code == 201
        assert create_from_account_response.json().get("balance") == 0


        replenishment_from_account_responce = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": from_account_id,
                "amount": 1500.5
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_from_user}",
                "Content-Type": "application/json"
            }
        )

        assert replenishment_from_account_responce.status_code == 200


        create_to_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": to_username,
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization" : f"Bearer {token}"
            }
        )

        assert create_to_user_response.status_code == 200
        assert create_to_user_response.json()["username"] == to_username
        assert create_to_user_response.json()["role"] == "ROLE_USER"


        login_to_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": to_username,
                "password": "Pas!sw0rd",
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )

        token_to_user = login_to_user_response.json().get("token")

        assert login_to_user_response.status_code == 200
        assert login_to_user_response.json()["user"]["username"] == to_username
        assert login_to_user_response.json()["user"]["role"] == "ROLE_USER"


        create_to_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_to_user}"
            }
        )

        to_account_id = create_to_account_response.json().get("id")

        assert create_to_account_response.status_code == 201
        assert create_to_account_response.json().get("balance") == 0


        transfer_account_responce = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={
                "fromAccountId": from_account_id,
                "toAccountId": to_account_id,
                "amount": amount
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token_from_user}",
                "Content-Type": "application/json",
            }
        )

        assert transfer_account_responce.status_code == 400









