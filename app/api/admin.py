from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from admin_config import admin_auth
from app.models import Account, Strategy, Trade
from app.schemas import StrategyCreate

router = APIRouter(prefix="/admin")

# ------------------------------------
# Delete all trades
# ------------------------------------
@router.delete("/trades")
def delete_all_trades(auth: bool = Depends(admin_auth), db: Session = Depends(get_db)):
    db.query(Trade).delete()
    db.commit()
    return {"status": "success", "message": "All trades deleted."}

# ------------------------------------
# Delete all accounts (cascades to trades)
# ------------------------------------
@router.delete("/accounts")
def delete_all_accounts(auth: bool = Depends(admin_auth), db: Session = Depends(get_db)):
    db.query(Account).delete()
    db.commit()
    return {"status": "success", "message": "All accounts deleted."}

# ------------------------------------
# Add new a strategy
# ------------------------------------
@router.post("/strategies", status_code = 201)
def create_strategy(payload: StrategyCreate, db: Session = Depends(get_db)):

    existing = db.query(Strategy).filter_by(name=payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Strategy already exists")
    
    strategy = Strategy(payload.model_dump())
    db.add(strategy)
    db.commit()
    db.refresh(strategy)

    return strategy