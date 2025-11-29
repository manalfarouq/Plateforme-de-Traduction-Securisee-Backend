#! Étape 1 : Utiliser une image Python 3.11
FROM python:3.11-slim

#! Étape 2 : Définir le dossier de travail dans le conteneur
WORKDIR /app

#! Étape 3 : Copier les fichiers requirements.txt
COPY requirements.txt .

#! Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

#! Étape 5 : Copier tout le code de l'app
COPY . .

#! Étape 6 : Exposer le port 8000
EXPOSE 8000

#! Étape 7 : Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]