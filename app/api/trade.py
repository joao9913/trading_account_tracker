from fastapi import Depends, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import Strategy, Trade, Account
from app.schemas import TradeCreate
import json
from sqlalchemy.exc import IntegrityError
from app.deps_auth import mt5_auth

router = APIRouter()

# ------------------------------------
# Insert a new trade
# ------------------------------------
@router.post("/mt5/trades", status_code=201, dependencies=[Depends(mt5_auth)])
async def create_trade(request: Request, db: Session = Depends(get_db)):
    raw = await request.body()
    data = json.loads(raw)
    payload = TradeCreate(**data)

    # Verify account exists
    account = db.get(Account, payload.account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account does not exist.")

    trade_data = payload.model_dump()
    current_balance = trade_data.pop("current_balance")

    trade = Trade(**trade_data)
    db.add(trade)

    account.current_balance = current_balance

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"status": "duplicate", "ticket_id": payload.ticket_id}

    db.refresh(trade)
    return trade

# ------------------------------------
# List all trades in the DB
# ------------------------------------
@router.get("/trades")
def get_trades(db: Session = Depends(get_db)):
    return db.query(Trade).all()

# ------------------------------------
# List all trades of a given account
# ------------------------------------
@router.get("/accounts/{account_id}/trades")
def get_trades_account(account_id: int, db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.account_id == account_id).all()

# ------------------------------------
# List all trades of given strategy
# ------------------------------------
@router.get("/strategies/{strategy_id}/trades")
def get_trades_strategy(strategy_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Trade)
        .join(Account)
        .filter(Account.strategy_id == strategy_id)
        .all()
    )