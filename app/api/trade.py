from fastapi import Depends, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import Strategy, Trade
from app.schemas import TradeCreate
from sqlalchemy import text
import json
from sqlalchemy.exc import IntegrityError

router = APIRouter()

# -------------------
# Insert a new trade
# -------------------
@router.post("/mt5/trades", status_code=201)
async def create_trade(request: Request, db: Session = Depends(get_db)):
    raw = await request.body()
    data = json.loads(raw)
    payload = TradeCreate(**data)

    strategy = db.get(Strategy, payload.strategy_id)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy does not exist.")

    trade_data = payload.model_dump()
    current_balance = trade_data.pop("current_balance")

    trade = Trade(**trade_data)
    db.add(trade)

    strategy.account.current_balance = current_balance

    try:
        db.commit()
    except IntegrityError:
        db.rollback() #duplicate trade detected
        return {"status": "duplicate", "ticket_id":payload.ticket_id}
    
    
    db.refresh(trade)
    return trade