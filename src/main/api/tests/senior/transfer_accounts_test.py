import pytest
from sqlalchemy.orm import Session

from src.main.api.db.crud.transaction_crud import TransactionCrudDb
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.classes.api_manager import ApiManager



@pytest.mark.api_senior
class TestTransferAccounts:
    def test_transfer_accounts_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = api_manager.user_steps.transfer_accounts(create_user_request, transfer_account_request)

        assert response.fromAccountIdBalance == 0

        transaction_from_db = TransactionCrudDb.get_transaction_by_id(db_session, transfer_account_request.toAccountId, transfer_account_request.fromAccountId)

        assert transaction_from_db.to_account_id == response.toAccountId, "Ошибка: Не найден ID аккаунта получателя"
        assert transaction_from_db.from_account_id == response.fromAccountId, "Ошибка: Не найден ID аккаунта отправителя"
        assert transaction_from_db.amount == transfer_account_request.amount, "Ошибка: Не найдено поле Amount"


    @pytest.mark.parametrize(
        "amount",
        [
            (499),
            (10001)
        ]
        )
    def test_transfer_accounts_invalid(self, api_manager, create_user_request, transfer_account_request, amount):
        transfer_account_request.amount = amount
        api_manager.user_steps.transfer_accounts_invalid(create_user_request, transfer_account_request)

