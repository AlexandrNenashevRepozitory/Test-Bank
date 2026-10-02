from typing import Annotated

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class DepositAccountRequest(BaseModel):
    accountId: int
    amount: float