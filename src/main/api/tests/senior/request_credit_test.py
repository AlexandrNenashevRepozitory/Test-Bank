import pytest
from sqlalchemy.orm import Session

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.request_credit_request import RequestCreditRequest


@pytest.mark.api_senior
class TestRequestCredit:
    def test_request_credit_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, request_credit_request: RequestCreditRequest):
        response = api_manager.user_steps.request_credit(create_credit_user_request, request_credit_request)

        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        assert credit_from_db.id is not None, 'Ошибка: Кредит не создан. ID кредита нет в БД'

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.balance >= request_credit_request.amount, 'Ошибка: Сумма кредита не поступила на баланс аккаунта'


    @pytest.mark.parametrize(
        "amount",
        [
            (4999),
            (15001)
        ]
        )
    def test_request_credit_invalid(self, api_manager, create_credit_user_request, request_credit_request, amount):
        request_credit_request.amount = amount
        api_manager.user_steps.request_credit_invalid(create_credit_user_request, request_credit_request)
