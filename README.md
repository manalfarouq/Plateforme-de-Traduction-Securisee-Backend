# Plateforme de Traduction Sécurisée - Backend

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)


## Description

API Backend FastAPI pour une plateforme de traduction sécurisée développée pour TalAIt. Cette API permet la traduction bidirectionnelle français-anglais via l'API Hugging Face, avec authentification JWT et gestion des utilisateurs.

**Frontend associé :** [Plateforme de Traduction Sécurisée - Frontend](https://github.com/manalfarouq/Plateforme-de-Traduction-Securisee-Frontend.git)


## Fonctionnalités

- ✅ **Authentification JWT** - Système complet d'inscription/connexion
- ✅ **Traduction IA** - Intégration avec Hugging Face (Helsinki-NLP models)
- ✅ **Gestion des utilisateurs** - Rôles user/admin avec code d'accès admin
- ✅ **Sécurité** - Hashage des mots de passe avec bcrypt
- ✅ **Base de données** - PostgreSQL pour le stockage persistant
- ✅ **CORS** - Configuration pour frontend distant
- ✅ **API RESTful** - Architecture claire et documentée
- ✅ **CI/CD** - Tests automatisés avec GitHub Actions
- ✅ **Docker** - Containerisation complète avec Docker Compose

## Technologies

- **Framework** : FastAPI 0.104+
- **Base de données** : PostgreSQL 15
- **Authentification** : JWT (python-jose)
- **Sécurité** : bcrypt, python-dotenv
- **IA** : Hugging Face Inference API (Helsinki-NLP)
- **Tests** : pytest, pytest-cov, pytest-asyncio
- **Conteneurisation** : Docker & Docker Compose
- **CI/CD** : GitHub Actions
- **Déploiement** : Render

## Installation

### Prérequis

- Python 3.11+
- PostgreSQL 15+
- Compte Hugging Face (pour le token API)
- Docker & Docker Compose (optionnel)

### 1. Cloner le repository

```bash
git clone https://github.com/manalfarouq/Plateforme-de-Traduction-Securisee-Backend.git
cd Plateforme-de-Traduction-Securisee-Backend
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine en vous basant sur `.env.example` :

```env
# Hugging Face
HF_TOKEN=hf_your_token_here

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=traduction_db
DB_USER=traduction_user
DB_PASSWORD=your_password

# JWT
SK=your_secret_key_here
ALG=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Render Database URL (production)
DATABASE_URL=postgresql://user:password@host/database
```

> **Sécurité** : Ne commitez JAMAIS le fichier `.env` sur GitHub !

### 5. Créer la base de données

```sql
-- Connectez-vous à PostgreSQL et exécutez :
CREATE DATABASE traduction_db;

-- Créez la table users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Donner les droits
GRANT ALL PRIVILEGES ON TABLE users TO traduction_user;
GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO traduction_user;
```

Ou utilisez le script fourni :

```bash
psql -U postgres -f init.sql
```

### 6. Lancer le serveur

```bash
uvicorn main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

## Installation avec Docker

### Option 1 : Docker Compose (Recommandé)

```bash
# Lancer tous les services
docker-compose up -d

# Vérifier les logs
docker-compose logs -f

# Arrêter les services
docker-compose down
```

Cette commande lance automatiquement :
- PostgreSQL sur le port 5432
- FastAPI sur le port 8000

### Option 2 : Docker seul

```bash
# Build l'image
docker build -t zorohack-backend .

# Lancer le conteneur
docker run -p 8000:8000 --env-file .env zorohack-backend
```

## Documentation API

### Base URL

```
Production: https://zorohack.onrender.com
Local: http://localhost:8000
Documentation: http://localhost:8000/docs
```

### Endpoints

#### 1. **Root**
```http
GET /
```
Retourne un message de bienvenue.

**Réponse :**
```json
{
  "message": "Bienvenue dans zoroTraduction!"
}
```

---

#### 2. **Inscription**
```http
POST /register/register
```

**Body :**
```json
{
  "username": "user123",
  "password": "password123",
  "role": "user",
  "admin_code": "2480"  // Optionnel, requis si role = "admin"
}
```

**Réponse :**
```json
{
  "message": "Utilisateur créé avec succès",
  "username": "user123",
  "role": "user",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Codes d'erreur :**
- `400` : Utilisateur existe déjà
- `403` : Code admin incorrect
- `500` : Erreur serveur

---

#### 3. **Connexion**
```http
POST /login/login
```

**Body :**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**Réponse :**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "user123",
  "role": "user"
}
```

**Codes d'erreur :**
- `401` : Identifiants incorrects
- `500` : Erreur serveur

---

#### 4. **Traduction FR → EN** (Protégé)
```http
POST /traduction/traduire/fr-en
```

**Headers :**
```
token: your_jwt_token_here
```

**Body :**
```json
{
  "text": "Bonjour le monde"
}
```

**Réponse :**
```json
{
  "success": true,
  "direction": "fr-en",
  "original_text": "Bonjour le monde",
  "translated_text": "Hello world"
}
```

---

#### 5. **Traduction EN → FR** (Protégé)
```http
POST /traduction/traduire/en-fr
```

**Headers :**
```
token: your_jwt_token_here
```

**Body :**
```json
{
  "text": "Hello world"
}
```

**Réponse :**
```json
{
  "success": true,
  "direction": "en-fr",
  "original_text": "Hello world",
  "translated_text": "Bonjour le monde"
}
```

**Codes d'erreur :**
- `401` : Token invalide ou expiré
- `500` : Erreur Hugging Face ou serveur

---

#### 6. **Liste des utilisateurs** (Admin uniquement)
```http
GET /admin/users
```

**Headers :**
```
token: your_admin_jwt_token_here
```

**Réponse :**
```json
{
  "users": [
    {
      "id": 1,
      "username": "admin",
      "role": "admin"
    },
    {
      "id": 2,
      "username": "user123",
      "role": "user"
    }
  ]
}
```

**Codes d'erreur :**
- `401` : Token manquant ou invalide
- `403` : Accès réservé aux admins

---

#### 7. **Test JWT**
```http
GET /data/TestJWT
```

**Headers :**
```
token: your_jwt_token_here
```

**Réponse :**
```json
{
  "message": "Token JWT valide!",
  "username": "user123"
}
```

## Sécurité

### Authentification JWT

- Les tokens expirent après 24 heures (configurable)
- Format du token dans le header : `token: <jwt_token>`
- Algorithme : HS256
- Payload contient : `sub` (username) et `role`

### Hashage des mots de passe

- Utilisation de **bcrypt** avec salt automatique
- Pas de stockage en clair
- Vérification sécurisée lors de la connexion

### Code Admin

- Code requis pour créer un compte admin : `2480`
- Les utilisateurs normaux ne peuvent pas s'auto-promouvoir
- Validation côté backend

### CORS

- Configuration permissive pour le développement (`allow_origins=["*"]`)
- À restreindre en production avec les domaines autorisés

## Tests

### Structure des tests

```
tests/
├── test_simple.py
```

### Lancer les tests

```bash
# Tous les tests
pytest tests/ -v
```

### CI/CD avec GitHub Actions

Les tests s'exécutent automatiquement :
- Sur chaque push vers `main` ou branches `feature/*`
- Sur chaque pull request vers `main`

Le workflow :
1. Configure Python 3.11
2. Installe PostgreSQL
3. Crée la base de données de test
4. Exécute tous les tests avec couverture
5. Génère un rapport de couverture

Voir le fichier `.github/workflows/test.yml` pour plus de détails.

### Exemples de tests avec cURL

```bash
# Test d'inscription
curl -X POST http://localhost:8000/register/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","role":"user"}'

# Test de connexion
curl -X POST http://localhost:8000/login/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'

# Test de traduction (avec token)
curl -X POST http://localhost:8000/traduction/traduire/fr-en \
  -H "Content-Type: application/json" \
  -H "token: YOUR_TOKEN_HERE" \
  -d '{"text":"Bonjour le monde"}'
```

### Avec Postman

1. Importez la collection fournie
2. Testez les endpoints dans l'ordre :
   - Register → Login → TestJWT → Traduction

## Structure du projet

```
backend/
├── .github/
│   └── workflows/
│       └── test.yml              # CI/CD GitHub Actions
├── app/
│   ├── auth/
│   │   └── token_auth.py         # Vérification JWT
│   ├── core/
│   │   └── config.py             # Configuration Pydantic
│   ├── database/
│   │   └── db_connection.py      # Connexion PostgreSQL
│   ├── routes/
│   │   ├── register_router.py    # Inscription
│   │   ├── login_router.py       # Connexion
│   │   ├── traduire_router.py    # Traduction
│   │   ├── get_data_router.py    # Test JWT
│   │   └── get_all_users_router.py # Admin
│   ├── schemas/
│   │   ├── User_schema.py        # Schéma utilisateur
│   │   ├── LoginRequest_schema.py # Schéma login
│   │   └── TextRequest.py        # Schéma traduction
│   └── services/
│       └── huggingface_service.py # API Hugging Face
├── tests/
│   └── test_simple.py
├── main.py                       # Point d'entrée FastAPI
├── Dockerfile                    # Image Docker
├── docker-compose.yml            # Orchestration Docker
├── init.sql                      # Script SQL d'initialisation
├── requirements.txt              # Dépendances Python
├── .env.example                  # Template variables d'env
├── .gitignore                    # Fichiers ignorés par Git
└── README.md                     # Documentation
```

## Déploiement sur Render

### Étapes de déploiement

1. **Créer un service PostgreSQL**
   - Allez sur [Render Dashboard](https://dashboard.render.com/)
   - Créez une nouvelle base PostgreSQL
   - Notez l'URL de connexion (Internal Database URL)

2. **Créer un service Web**
   - Connectez votre repository GitHub
   - Type : Web Service
   - Runtime : Python 3
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `uvicorn main:app --host 0.0.0.0 --port 8000`

3. **Configurer les variables d'environnement**
   
   Dans les paramètres du service Web, ajoutez :
   
   ```
   HF_TOKEN=votre_token_huggingface
   SK=votre_secret_jwt
   ALG=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   DATABASE_URL=postgresql://user:pass@host/db  # URL de la base Render
   ```

4. **Déployer**
   - Render détecte automatiquement les changements
   - Le déploiement prend ~5 minutes
   - Votre API sera accessible sur : `https://votre-app.onrender.com`

### Configuration de la base de données sur Render

Render fournit une variable `DATABASE_URL`. Le code détecte automatiquement si cette variable existe et l'utilise en priorité :

```python
# Dans db_connection.py
database_url = os.getenv("DATABASE_URL")

if database_url:
    # Production (Render)
    conn = psycopg2.connect(database_url)
else:
    # Développement local
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        # ...
    )
```

### Initialiser la base de données

Connectez-vous au shell PostgreSQL sur Render et exécutez :

```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);
```

## Configuration avancée

### Variables d'environnement

| Variable | Description | Valeur par défaut | Requis |
|----------|-------------|-------------------|--------|
| `HF_TOKEN` | Token API Hugging Face | - | ✅ |
| `SK` | Secret key JWT | - | ✅ |
| `ALG` | Algorithme JWT | HS256 | ❌ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Durée validité token | 60 | ❌ |
| `DB_HOST` | Hôte PostgreSQL | localhost | ✅ |
| `DB_PORT` | Port PostgreSQL | 5432 | ✅ |
| `DB_NAME` | Nom base de données | traduction_db | ✅ |
| `DB_USER` | Utilisateur PostgreSQL | - | ✅ |
| `DB_PASSWORD` | Mot de passe PostgreSQL | - | ✅ |
| `DATABASE_URL` | URL complète PostgreSQL (Render) | - | ❌ |

### Générer une clé secrète JWT

```bash
# Avec OpenSSL
openssl rand -hex 32

# Avec Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Obtenir un token Hugging Face

1. Créez un compte sur [Hugging Face](https://huggingface.co/)
2. Allez dans Settings → Access Tokens
3. Créez un nouveau token avec les permissions "Read"
4. Copiez le token dans votre `.env`



## Remerciements

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderne
- [Hugging Face](https://huggingface.co/) - Modèles de traduction IA
- [Helsinki-NLP](https://huggingface.co/Helsinki-NLP) - Modèles OPUS-MT
- [PostgreSQL](https://www.postgresql.org/) - Base de données robuste
- [Render](https://render.com/) - Plateforme de déploiement


## Liens utiles

- **Frontend du projet** : [Plateforme de Traduction Sécurisée - Frontend](https://github.com/manalfarouq/Plateforme-de-Traduction-Securisee-Frontend.git)
- **API Documentation** : [https://zorohack.onrender.com/docs](https://zorohack.onrender.com/docs)
- **Repository Backend** : [GitHub](https://github.com/manalfarouq/Plateforme-de-Traduction-Securisee-Backend.git)

