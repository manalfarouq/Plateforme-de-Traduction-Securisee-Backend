from fastapi import APIRouter, HTTPException
from app.schemas.User_schema import user_schema
from app.database.db_connection import get_db_connection  
import bcrypt
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings


router = APIRouter(prefix="/register", tags=["SignUp"])


@router.post("/register")
def register(data: user_schema):
    """
    Endpoint pour l'inscription des nouveaux utilisateurs.
    Vérifie que le username n'existe pas déjà et crée un nouveau compte.
    Route simple de signup :
    - Vérifie si le username existe déjà
    - Hash le mot de passe avec bcrypt
    - Insère le nouvel utilisateur dans la base
    - Retourne un message de succès
    - Si role = "user" : inscription directe
    - Si role = "admin" : vérification du code 2480
    """
    
    # Connexion à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        #! 1. Vérifier le code admin si le rôle est "admin"
        if data.role == "admin":
            if data.admin_code != "2480":
                raise HTTPException(status_code=403, detail="Code admin incorrect")
        
        #! 2. Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT username FROM users WHERE username = %s", (data.username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Ce nom d'utilisateur existe déjà.")
        
        #! 3. Hasher le mot de passe avec bcrypt
        hashed_password = bcrypt.hashpw(data.password.encode('utf-8'), bcrypt.gensalt())
        
        #! 4. Insérer le nouvel utilisateur avec le rôle choisi
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (data.username, hashed_password.decode('utf-8'), data.role)
        )
        
        #! 5. Sauvegarder les changements dans la base
        conn.commit()
        
        #! 6. Créer un JWT token
        expire = datetime.now(timezone.utc) + timedelta(hours=24)
        token = jwt.encode(
            {"sub": data.username, "role": data.role, "exp": expire},settings.SK,algorithm=settings.ALG)
        
        #! 7. Retourner un message de succès avec token
        return {
            "message": "Utilisateur créé avec succès",
            "username": data.username,
            "role": data.role,
            "token": token
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        conn.close()