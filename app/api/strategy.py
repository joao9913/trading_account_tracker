from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import Account, Strategy, Trade

router = APIRouter()

# ------------------------------------
# List all strategies
# ------------------------------------
@router.get("/strategies")
def get_strategies(db: Session = Depends(get_db)):
    return db.query(Strategy).all()

# ------------------------------------
# List a single strategy
# ------------------------------------
@router.get("/strategies/{strategy_id}")
def get_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(Trade).join(Account).filter(Account.strategy_id == strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy

# ------------------------------------
# List a single strategy of a given account
# ------------------------------------
@router.get("/accounts/{account_id}/strategy")
def get_strategy_account(account_id: int, db: Session = Depends(get_db)):
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account.strategy