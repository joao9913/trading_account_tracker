from fastapi import FastAPI, Header, HTTPException, Depends
from app.api import account, trade, strategy, admin
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware

if settings.ENV == "production":
    app = FastAPI(
        title = "Account Tracker",
        docs_url = None,
        redoc_url=None,
        openapi_url=None,
    )
else:
    app = FastAPI(title="Account Tracker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENV != "production" else [],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def mt5_auth(x_api_key: str = Header(...)):
    if x_api_key != settings.MT5_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

app.include_router(account.router, prefix="/accounts", tags=["Accounts"])
app.include_router(strategy.router, prefix="/strategy", tags=["Strategies"])
app.include_router(trade.router, prefix="/trade", tags=["Trades"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.get("/", tags=["Root"])
def root():
    return {"status": "ok"}