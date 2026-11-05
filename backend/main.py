from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.database import engine
from backend.routers.notes import router as notes_router
from backend.routers.auth import router as auth_router

app = FastAPI(
    title="NoteSpace API",
    description="API de gestion des notes",
    version="1.0.0"
)

# Routes d'authentification
app.include_router(auth_router)

# Routes de gestion des notes
app.include_router(notes_router)


@app.get("/", tags=["Accueil"])
def accueil():
    return {
        "message": "Bienvenue sur NoteSpace API",
        "status": "running"
    }


@app.get("/health/db", tags=["Health"])
def verifier_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "notespace_db",
            "status": "connected"
        }

    except SQLAlchemyError:
        return {
            "status": "error",
            "message": "Connexion à la base impossible"
        }
