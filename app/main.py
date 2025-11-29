from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.traduire_router import router as traduire_router
from app.routes.login_router import router as login_router
from app.routes.get_data_router import router as get_data_router
from app.routes.register_router import router as register_router
from app.routes.get_all_users_router import router as get_all_users_router

app = FastAPI(title="Traduction Sécurisée avec Authentification JWT")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Bienvenue dans zoroTraduction!",}


# Inclure les routers dans un ordre logique
app.include_router(register_router)  # Inscription d'abord
app.include_router(login_router)     # Puis connexion
app.include_router(get_data_router)  # Récupération de données
app.include_router(get_all_users_router)  # Opérations admin
app.include_router(traduire_router)  # Fonctionnalité principale