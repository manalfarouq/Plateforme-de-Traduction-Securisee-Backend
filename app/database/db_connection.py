import psycopg2
import os
from app.core.config import settings

"""
Qu'est-ce que ça fait ?

=> Cette fonction crée une connexion entre Python et PostgreSQL
=> C'est comme ouvrir une porte entre le code et la base de données
=> Chaque fois que je veux lire/écrire dans la base, j'appelle cette fonction
=> Fonctionne en local ET sur Render
"""

def get_db_connection():
    # Utiliser DATABASE_URL si disponible (Render)
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Sur Render - Utiliser l'URL complète
        print("Connexion à la base de données Render")
        conn = psycopg2.connect(database_url)
    else:
        # En local - Utiliser les paramètres individuels
        print("Connexion à la base de données locale")
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
    
    return conn