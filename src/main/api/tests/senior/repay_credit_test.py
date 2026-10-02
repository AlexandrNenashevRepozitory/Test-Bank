import pytest
from sqlalchemy.orm import Session

from src.archive.middle.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.repay_credit_request import RepayCreditRequest


@pytest.mark.api_senior
class TestRepayCredit:
    def test_repay_credit_valid(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        repay_response = api_manager.user_steps.repay_credit(create_credit_user_request, repay_credit_request)

        assert repay_credit_request.amount == repay_response.amountDeposited
        assert repay_credit_request.creditId == repay_response.creditId

        credit_from_db = Credit.get_credit_by_id(db_session, repay_response.creditId)
        assert credit_from_db.id == repay_response.creditId, 'Ошибка БД: Ответ CreditId не совпадает с CreditId в БД'
        assert credit_from_db.amount == repay_response.amountDeposited, 'Ошибка БД: Сумма погашения не совпадает с БД'
        assert credit_from_db.balance == 0, 'Ошибка БД: Кредит погашен не полностью'



    @pytest.mark.parametrize(
        "amount",
        [
            (10001),
            (9999)
        ]
        )
    def test_repay_credit_invalid(self, api_manager, create_credit_user_request, repay_credit_request, amount):
        repay_credit_request.amount = amount
        api_manager.user_steps.repay_credit_invalid(create_credit_user_request, repay_credit_request)

