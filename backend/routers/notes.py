
import os
import requests

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.note import Note
from backend.models.user import User
from backend.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from backend.dependencies import get_current_user


router = APIRouter(prefix="/notes", tags=["Notes"])

REALTIME_URL = "http://127.0.0.1:8765/publish"

REALTIME_SECRET = os.getenv(
    "NOTESPACE_REALTIME_SECRET",
    "notespace-local-dev-secret"
)


def notifier_evenement(action, note, user):
    """Envoie une notification à Tornado après une opération sur une note."""

    evenement = {
        "type": "note",
        "action": action,
        "note_id": note.id,
        "title": note.title,
        "user_id": user.id
    }

    try:
        requests.post(
            REALTIME_URL,
            json=evenement,
            headers={
                "X-Notespace-Secret": REALTIME_SECRET
            },
            timeout=2
        )
    except requests.RequestException as error:
        print(f"Notification Tornado indisponible : {error}")


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED
)
def creer_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        category=note_data.category,
        user_id=current_user.id
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    notifier_evenement("created", note, current_user)

    return note


@router.get("/", response_model=list[NoteResponse])
def afficher_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Note)
        .filter(Note.user_id == current_user.id)
        .order_by(Note.created_at.desc())
        .all()
    )


@router.get("/{note_id}", response_model=NoteResponse)
def obtenir_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note introuvable"
        )

    return note


@router.put("/{note_id}", response_model=NoteResponse)
def modifier_note(
    note_id: int,
    note_data: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note introuvable"
        )

    modifications = note_data.model_dump(exclude_unset=True)

    for champ, valeur in modifications.items():
        setattr(note, champ, valeur)

    db.commit()
    db.refresh(note)

    notifier_evenement("updated", note, current_user)

    return note


@router.delete("/{note_id}")
def supprimer_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note introuvable"
        )

    note_supprimee = {
        "id": note.id,
        "title": note.title
    }

    db.delete(note)
    db.commit()

    class NoteSupprimee:
        pass

    evenement = NoteSupprimee()
    evenement.id = note_supprimee["id"]
    evenement.title = note_supprimee["title"]

    notifier_evenement("deleted", evenement, current_user)

    return {
        "message": "Note supprimée avec succès"
    }
