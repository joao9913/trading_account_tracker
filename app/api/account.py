from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import Account, Strategy, Trade
from app.schemas import AccountCreate

router = APIRouter()

# ------------------------------------
# Insert a new account
# ------------------------------------
@router.post("/accounts", status_code = 201)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)):
    existing = db.get(Account, payload.id)
    if existing:
        raise HTTPException(status_code=409, detail="Account already exists")
    
    # Find predefined strategy by name
    strategy = db.query(Strategy).filter_by(name=payload.strategy_name).first()
    if not strategy:
        raise HTTPException(status_code = 404, detail=f"Strategy '{payload.strategy_name}' not found") 
    
    account_data = payload.model_dump()
    account_data["strategy_id"] = strategy.id
    account = Account(**account_data)

    account = Account(**account_data)

    db.add(account)
    db.commit()
    db.refresh(account)

    return account

# ------------------------------------
# List all accounts 
# ------------------------------------
@router.get("/accounts")
def get_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()

# ------------------------------------
# List details of a single account
# ------------------------------------
@router.get("/accounts/{account_id}/trades")
def get_trades_account(account_id: int, db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.account_id == account_id).all()