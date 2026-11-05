from backend.database import Base, engine
from backend.models import User, Note


def init_database():
    print("Création des tables NoteSpace...")

    Base.metadata.create_all(bind=engine)

    print("Tables créées avec succès !")


if __name__ == "__main__":
    init_database()
