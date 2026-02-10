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
    account_id: int
    name: str

class TradeCreate(BaseModel):
    strategy_id: int
    symbol: str
    pnl: float
    open_datetime: date
    close_datetime: date
    ticket_id: int
    current_balance: float