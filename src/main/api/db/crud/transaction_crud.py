from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction



class TransactionCrudDb:
    @staticmethod
    def get_transaction_by_id(db: Session, to_account_id: int, from_account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=to_account_id, from_account_id=from_account_id).first()