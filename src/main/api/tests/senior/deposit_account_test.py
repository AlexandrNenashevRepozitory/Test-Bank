import pytest
from sqlalchemy.orm import Session

from src.archive.middle.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_account_request import DepositAccountRequest


@pytest.mark.api_senior
class TestDepositAccount:
    def test_deposit_account_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)

        assert deposit_account_request.amount == response.balance
        assert deposit_account_request.accountId == response.id

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Ошибка: ID аккаунтов не совпадают'
        assert account_from_db.balance >= deposit_account_request.amount, 'Ошибка: Баланс аккаунта меньше суммы пополнения'


    @pytest.mark.parametrize(
        "amount",
        [
            (999),
            (10001)
        ]
        )
    def test_deposit_account_invalid(self, api_manager, create_user_request, deposit_account_request, amount):
        deposit_account_request.amount = amount
        api_manager.user_steps.deposit_account_invalid(create_user_request, deposit_account_request)






