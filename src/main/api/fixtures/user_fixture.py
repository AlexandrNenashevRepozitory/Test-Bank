import pytest

from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.request_credit_request import RequestCreditRequest



@pytest.fixture
def create_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)

    return user_request

@pytest.fixture
def second_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    api_manager.admin_steps.create_user(user_request)

    return user_request

@pytest.fixture
def create_credit_user_request(api_manager):
    user_request = RandomModelGenerator.generate(CreateUserRequest)
    user_request.role = "ROLE_CREDIT_SECRET"
    api_manager.admin_steps.create_user(user_request)

    return user_request

@pytest.fixture
def request_credit_request(api_manager, create_credit_user_request):
    account = api_manager.user_steps.create_account(create_credit_user_request)

    return RequestCreditRequest(
        accountId = account.id,
        amount = 10000,
        termMonths = 12
    )

@pytest.fixture
def repay_credit_request(api_manager, create_credit_user_request, request_credit_request):
    response_credit = api_manager.user_steps.request_credit(create_credit_user_request, request_credit_request)

    return RepayCreditRequest(
        creditId = response_credit.creditId,
        accountId = request_credit_request.accountId,
        amount = response_credit.amount
    )

@pytest.fixture
def deposit_account_request(api_manager, create_user_request):
    account = api_manager.user_steps.create_account(create_user_request)

    return DepositAccountRequest(
        accountId = account.id,
        amount = 5000
    )

@pytest.fixture
def transfer_account_request(api_manager, create_user_request, second_user_request, deposit_account_request):
    from_account = api_manager.user_steps.create_account(create_user_request)
    to_account = api_manager.user_steps.create_account(second_user_request)

    api_manager.user_steps.deposit_account(
        create_user_request,
        DepositAccountRequest(
            accountId=from_account.id,
            amount=5000
        )
    )

    return TransferAccountRequest(
        fromAccountId = from_account.id,
        toAccountId = to_account.id,
        amount = 5000
    )




