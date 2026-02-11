from fastapi import FastAPI
from app.api import account, trade, strategy

app = FastAPI(title = "Account Tracker")

app.include_router(account.router, prefix="/accounts", tags=["Accounts"])
app.include_router(strategy.router, prefix="/strategy", tags=["Strategies"])
app.include_router(trade.router, prefix="/trade", tags=["Trades"])