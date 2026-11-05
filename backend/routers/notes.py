from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.note import Note
from backend.models.user import User
from backend.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from backend.dependencies import get_current_user

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


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
        raise HTTPException(status_code=404, detail="Note introuvable")

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
        raise HTTPException(status_code=404, detail="Note introuvable")

    modifications = note_data.model_dump(exclude_unset=True)

    for champ, valeur in modifications.items():
        setattr(note, champ, valeur)

    db.commit()
    db.refresh(note)

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
        raise HTTPException(status_code=404, detail="Note introuvable")

    db.delete(note)
    db.commit()

    return {"message": "Note supprimée avec succès"}
