from pydantic import BaseModel
from datetime import date, datetime

class AccountCreate(BaseModel):
    id: int
    owner: str
    starting_balance: float
    profit_target: float
    max_drawdown: float
    starting_date: date
    account_status: str
    strategy_id: int

class AccountRead(BaseModel):
    id: int
    owner: str
    starting_balance: float
    current_balance: float
    profit_target: float
    max_drawdown: float
    starting_date: date
    ending_date: date | None
    account_status: str
    strategy: StrategyRead

    class Config:
        from_attributes = True

class StrategyCreate(BaseModel):
    name: str

class StrategyRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TradeCreate(BaseModel):
    account_id: int
    symbol: str
    pnl: float
    open_datetime: datetime
    close_datetime: datetime
    ticket_id: int
    current_balance: float

class TradeRead(BaseModel):
    id: int
    account_id: int
    symbol: str
    pnl: float
    open_datetime: datetime
    close_datetime: datetime

    class Config:
        from_attributes = True