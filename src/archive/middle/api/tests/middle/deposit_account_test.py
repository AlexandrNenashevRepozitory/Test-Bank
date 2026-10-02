import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.responce_specs import ResponseSpecs


@pytest.mark.api_middle
class TestDepositAccount:
    def test_deposit_account_valid(self):
        create_user_request = CreateUserRequest(username="Max400", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max400", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        assert create_account_response.balance == 0

        accountId = create_account_response.id

        deposit_account_request = DepositAccountRequest(accountId=accountId, amount=1500)
        response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max400", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)


        assert deposit_account_request.amount == response.balance
        assert deposit_account_request.accountId == accountId




    @pytest.mark.parametrize(
        "username, amount",
        [
            ("Max401", 999.0),
            ("Max402", 10001.0)
        ]
        )
    def test_deposit_account_invalid(self, username, amount):
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        create_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        accountId = create_account_response.id

        deposit_account_request = DepositAccountRequest(accountId=accountId, amount=amount)
        DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(deposit_account_request)





