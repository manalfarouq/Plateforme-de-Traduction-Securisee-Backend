from fastapi import APIRouter, HTTPException, Header
from app.database.db_connection import get_db_connection
from app.core.config import settings
from jose import jwt 

router = APIRouter(prefix="/admin", tags=["Admin Operations"])   

@router.get("/users")
def get_all_users(token: str = Header(...)):
    """
    Endpoint pour récupérer tous les utilisateurs (ADMIN ONLY)
    """
    # Vérifier que l'utilisateur est admin
    if not token:
        raise HTTPException(status_code=401, detail="Token manquant")
    
    try:
        payload = jwt.decode(token, settings.SK, algorithms=[settings.ALG])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Accès réservé aux admins")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Ne sélectionner que les colonnes existantes dans ta DB
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        
        return {
            "users": [
                {
                    "id": user[0],
                    "username": user[1],
                    "role": user[2],
                }
                for user in users
            ]
        }
    finally:
        cursor.close()
        conn.close()
