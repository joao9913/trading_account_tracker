from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.database import ADMIN_PASSWORD
import secrets

security = HTTPBasic()

def admin_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not secrets.compare_digest(credentials.password, ADMIN_PASSWORD):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Unnauthorized",
            headers = {"WWW-Authenticate": "Basic"},
        )
    return True