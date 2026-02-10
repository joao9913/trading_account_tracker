from pydantic import BaseModel
from datetime import date

class AccountCreate(BaseModel):
    id: int
    owner: str
    starting_balance: float
    current_balance: float
    profit_target: float
    max_drawdown: float
    starting_date: date

class StrategyCreate(BaseModel):
    id: int
    account_id: int
    name: str

class TradeCreate(BaseModel)