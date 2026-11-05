from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.models.user import User


def create_demo_user():
    db: Session = SessionLocal()

    try:
        user = db.query(User).filter(
            User.id == 1
        ).first()

        if user:
            print("Utilisateur de démonstration déjà existant.")
            return

        user = User(
            id=1,
            username="demo",
            email="demo@notespace.local",
            hashed_password="DEMO_ACCOUNT_NOT_FOR_LOGIN",
            is_active=True
        )

        db.add(user)
        db.commit()

        print("Utilisateur de démonstration créé !")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_demo_user()
