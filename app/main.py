from fastapi import FastAPI, Depends, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import Account, Strategy, Trade
from app.schemas import AccountCreate, StrategyCreate, TradeCreate
from sqlalchemy import text
import json
from sqlalchemy.exc import IntegrityError

app = FastAPI()

# ACCOUNT GET ENDPOINTS

@app.get("/accounts")
def get_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()

# STRATEGY GET ENDPOINTS

@app.get("/strategies")
def get_strategies(db: Session = Depends(get_db)):
    return db.query(Strategy).all()

@app.get("/accounts/{account_id}/strategies")
def get_strategies_account(account_id: int, db: Session = Depends(get_db)):
    return db.query(Strategy).filter(Strategy.account_id == account_id).all()

# TRADE GET ENDPOINTS

@app.get("/trades")
def get_trades(db: Session = Depends(get_db)):
    return db.query(Trade).all()

@app.get("/accounts/{account_id}/trades")
def get_trades_account(account_id: int, db:Session = Depends(get_db)):
    trades = (db.query(Trade).join(Strategy, Trade.strategy_id == Strategy.id).filter(Strategy.account_id == account_id)).all()
    return trades


# ACCOUNT POST ENDPOINTS
@app.post("/accounts", status_code = 201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    existing = db.get(Account, payload.id)
    if existing:
        raise HTTPException(status_code=409, detail="Account already exists")
    
    account = Account(**payload.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)

    return account

# STRATEGY POST ENDPOINTS
@app.post("/strategies", status_code = 201)
def create_strategy(payload: StrategyCreate, db: Session = Depends(get_db)):    
    account_exists = db.get(Account, payload.account_id)
    if not account_exists:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    strategy = Strategy(**payload.model_dump())
    db.add(strategy)
    db.commit()
    db.refresh(strategy)

    return strategy

