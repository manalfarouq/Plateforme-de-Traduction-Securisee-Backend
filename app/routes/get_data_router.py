from fastapi import APIRouter, HTTPException, Header
from app.core.config import settings
from jose import jwt
from jose.exceptions import JWTError

router = APIRouter(prefix="/data", tags=["Test du token JWT"])

@router.get("/TestJWT")
def get_data(token: str = Header(...)):
    """
    Vérifie le token JWT passé directement dans le header.
    Format attendu : "<token>"
    """
    try:
        payload = jwt.decode(token, settings.SK, algorithms = [settings.ALG])
    except JWTError:
        raise HTTPException(status_code=401,detail="Token JWT invalide ou expiré.")    
    
    return {
        "message": "Token JWT valide!", 
        "username": payload.get("sub")}