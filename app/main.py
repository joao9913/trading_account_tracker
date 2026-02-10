from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.deps import get_db
from app.models import Account

app = FastAPI()

@app.get("/accounts")
def get_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()