import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.repay_credit_requester import RepayCreditRequester
from src.main.api.requests.request_credit_requester import RequestCreditRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.responce_specs import ResponseSpecs


@pytest.mark.api_middle
class TestRepayCredit:
    def test_repay_credit_valid(self):
        create_user_request = CreateUserRequest(username="Max700", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max700", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id = response.id

        request_credit_request = RequestCreditRequest(accountId=account_id, amount=10000, termMonths=12)

        response = RequestCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max700", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(request_credit_request)

        credit_id = response.creditId

        repay_credit_request = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=10000)

        RepayCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max700", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(repay_credit_request)

    def test_repay_credit_invalid(self):
        create_user_request = CreateUserRequest(username="Max701", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max701", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        account_id = response.id

        request_credit_request = RequestCreditRequest(accountId=account_id, amount=10000, termMonths=12)

        response = RequestCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max701", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(request_credit_request)

        credit_id = response.creditId

        repay_credit_request = RepayCreditRequest(creditId=credit_id, accountId=account_id, amount=100)

        RepayCreditRequester(
            request_spec=RequestSpecs.auth_headers(username="Max701", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_unprocessable_entity()
        ).post(repay_credit_request)

