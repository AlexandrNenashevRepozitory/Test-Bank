from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.responce_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps



class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created()
        ).post()
        return response

    def request_credit(self, create_user_request: CreateUserRequest, request_credit_request: RequestCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_created()
        ).post(request_credit_request)
        return response

    def request_credit_invalid(self, create_credit_user_request: CreateUserRequest, request_credit_request: RequestCreditRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_bad()
        ).post(request_credit_request)

    def repay_credit(self, create_credit_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok()
        ).post(repay_credit_request)
        return response

    def repay_credit_invalid(self, create_credit_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_credit_user_request.username, password=create_credit_user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_unprocessable_entity()
        ).post(repay_credit_request)

    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def deposit_account_invalid(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad()
        ).post(deposit_account_request)

    def transfer_accounts(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = ValidateCrudRequester(
         RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNTS,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response

    def transfer_accounts_invalid(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        CrudRequester(
         RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNTS,
            ResponseSpecs.request_bad()
        ).post(transfer_account_request)