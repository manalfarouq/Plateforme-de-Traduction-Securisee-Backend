from app.schemas.LoginRequest_schema import LoginRequest
from fastapi import APIRouter, HTTPException
from app.database.db_connection import get_db_connection
import bcrypt
from jose import jwt
from app.core.config import settings


router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/login")
def login(data: LoginRequest):
    """
    Endpoint pour la connexion des utilisateurs.
    Vérifie les informations d'identification et retourne un token JWT si valides.
    """
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Chercher l'utilisateur par username
        cursor.execute("SELECT id, username, password, role FROM users WHERE username = %s", (data.username,))
        user = cursor.fetchone()
        
        if user is None:
            raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect.")
        
        # Récupérer les données (attention à l'ordre : id, username, password, role)
        user_id, db_username, db_password, db_role = user
        
        # 2. Vérifier le mot de passe avec bcrypt
        # db_password est une string stockée en base, on l'encode en bytes
        if not bcrypt.checkpw(data.password.encode('utf-8'), db_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect.")
        
        # 3. Générer un token JWT avec jose
        payload = {
            "sub": db_username,
            "role": db_role
        }
        
        token = jwt.encode(payload, settings.SK, algorithm=settings.ALG)
        
        # 4. Retourner le token
        return {
            "token": token,
            "user_id": user_id,
            "username": db_username,
            "role": db_role
        }

    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()