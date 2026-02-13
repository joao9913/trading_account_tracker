from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = set(filter(None, [os.getenv("API_KEY_RUBEN"), os.getenv("ADMIN_PASSWORD")]))
MT5_API_KEY = os.getenv("MT5_API_KEY")

def api_key_auth(x_api_key: str = Header(..., alias="X-API-KEY")):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

def mt5_auth(x_api_key: str = Header()):
    if x_api_key != MT5_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True