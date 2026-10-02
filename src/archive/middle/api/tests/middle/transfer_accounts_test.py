import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.transfer_account_requester import TransferAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.responce_specs import ResponseSpecs


@pytest.mark.api_middle
class TestTransferAccounts:
    def test_transfer_accounts_valid(self):

        create_user_out_request = CreateUserRequest(username="Max500", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_out_request)

        create_out_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max500", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        from_account_id = create_out_account_response.id


        create_user_in_request = CreateUserRequest(username="Max501", password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_in_request)

        create_in_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max501", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        to_account_id = create_in_account_response.id


        deposit_account_request = DepositAccountRequest(accountId=from_account_id, amount=3500)
        DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max500", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)


        transfer_account_request = TransferAccountRequest(fromAccountId=from_account_id, toAccountId=to_account_id, amount=2000)

        transfer_account_response = TransferAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max500", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_account_request)

        assert transfer_account_response.fromAccountIdBalance == 1500


    @pytest.mark.parametrize(
        "from_username, to_username, amount",
        [
            ("Max502", "Max503", 499),
            ("Max504", "Max505", 10001)
        ]
        )
    def test_transfer_accounts_invalid(self, from_username, to_username, amount):

        create_user_out_request = CreateUserRequest(username=from_username, password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_out_request)

        create_out_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=from_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        from_account_id = create_out_account_response.id


        create_user_in_request = CreateUserRequest(username=to_username, password="Pas!sw0rd", role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_in_request)

        create_in_account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=to_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        to_account_id = create_in_account_response.id


        deposit_account_request = DepositAccountRequest(accountId=from_account_id, amount=3500)
        DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=from_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(deposit_account_request)


        transfer_account_request = TransferAccountRequest(fromAccountId=from_account_id, toAccountId=to_account_id, amount=amount)

        TransferAccountRequester(
            request_spec=RequestSpecs.auth_headers(username=from_username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_account_request)
