import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.db_connection import get_db_connection

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Prépare la DB avant chaque test"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Crée la table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL
            );
        """)
        conn.commit()
        
        # Vide la table
        cur.execute("DELETE FROM users;")
        conn.commit()
    finally:
        cur.close()
        conn.close()
    
    yield
    
    # Cleanup
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM users;")
        conn.commit()
    finally:
        cur.close()
        conn.close()


# ==================== TEST 1 : LOGIN ====================

def test_login_success():
    """
    Test simple : Un utilisateur se connecte avec les bons identifiants
    """
    # 1. Créer un utilisateur
    client.post(
        "/register/register",
        json={
            "username": "amina",
            "password": "password123",
            "role": "user"
        }
    )
    
    # 2. Se connecter
    response = client.post(
        "/login/login",
        json={
            "username": "amina",
            "password": "password123"
        }
    )
    
    # 3. Vérifier que ça marche
    assert response.status_code == 200
    assert "token" in response.json()


# ==================== TEST 2 : ACCÈS PROTÉGÉ SANS TOKEN ====================

def test_protected_route_without_token():
    """
    Test simple : Essayer d'accéder à une route protégée SANS token
    Doit échouer avec erreur 422 (token manquant)
    """
    response = client.get("/data/TestJWT")
    
    assert response.status_code == 422
