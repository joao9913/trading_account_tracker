from fastapi import FastAPI, Header, HTTPException, Depends, Request, APIRouter
from app.api import account, trade, strategy, admin
from fastapi.responses import JSONResponse
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware
import logging
import psycopg2

if settings.ENV == "production":
    app = FastAPI(
        title = "Account Tracker",
        docs_url = None,
        redoc_url=None,
        openapi_url=None,
    )
else:
    app = FastAPI(title="Account Tracker")

logger = logging.getLogger("uvicorn.error")

@app.exception_handler(Exception)
async def global_esception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception at {request.url}: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


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

router = APIRouter()

@router.get("/db-test")
def db_test():
    import os
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        conn.close()
        return {"db_test": result[0]}
    except Exception as e:
        return {"error": str(e)}

app.include_router(router, prefix="", tags=["Test"])