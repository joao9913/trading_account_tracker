from pydantic import BaseModel
from datetime import date, datetime

class AccountCreate(BaseModel):
    id: int
    owner: str
    starting_balance: float
    current_balance: float
    profit_target: float
    max_drawdown: float
    starting_date: date
    final_date: date
    account_status: str
    strategy_name: str

class StrategyCreate(BaseModel):
    account_id: int
    name: str

class TradeCreate(BaseModel):
    account_id: int
    strategy_id: int
    symbol: str
    pnl: float
    open_datetime: datetime
    close_datetime: datetime
    ticket_id: int
    current_balance: float