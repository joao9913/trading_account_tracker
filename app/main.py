from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import Account
from app.schemas import AccountCreate

app = FastAPI()

@app.get("/accounts")
def get_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()


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