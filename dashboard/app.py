
import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="NoteSpace",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# DESIGN
# =========================

st.markdown("""
<style>
.stApp {
    background-color: #F5F6FA;
}
.block-container {
    padding-top: 2rem;
}
[data-testid="stSidebar"] {
    background-color: white;
}
.main-title {
    font-size: 34px;
    font-weight: 800;
    color: #252B42;
}
.subtitle {
    color: #85899B;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


# =========================
# SESSION
# =========================

if "token" not in st.session_state:
    st.session_state.token = None

if "username" not in st.session_state:
    st.session_state.username = None


def get_headers():
    return {
        "Authorization": f"Bearer {st.session_state.token}"
    }


# =========================
# AUTHENTIFICATION
# =========================

def login(email, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            data={
                "username": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.session_state.username = email
            return True, None

        if response.status_code == 401:
            return False, "Email ou mot de passe incorrect."

        return False, response.text

    except requests.RequestException as error:
        return False, str(error)


def logout():
    st.session_state.token = None
    st.session_state.username = None
    st.rerun()


# =========================
# API NOTES
# =========================

def load_notes():
    try:
        response = requests.get(
            f"{API_URL}/notes/",
            headers=get_headers(),
            timeout=10
        )

        if response.status_code == 401:
            return None, "Session expirée."

        response.raise_for_status()
        return response.json(), None

    except requests.RequestException as error:
        return None, str(error)


def create_note(title, content, category):
    try:
        response = requests.post(
            f"{API_URL}/notes/",
            headers=get_headers(),
            json={
                "title": title,
                "content": content,
                "category": category
            },
            timeout=10
        )

        response.raise_for_status()
        return True, None

    except requests.RequestException as error:
        return False, str(error)


def update_note(note_id, title, content, category):
    try:
        response = requests.put(
            f"{API_URL}/notes/{note_id}",
            headers=get_headers(),
            json={
                "title": title,
                "content": content,
                "category": category
            },
            timeout=10
        )

        response.raise_for_status()
        return True, None

    except requests.RequestException as error:
        return False, str(error)


def delete_note(note_id):
    try:
        response = requests.delete(
            f"{API_URL}/notes/{note_id}",
            headers=get_headers(),
            timeout=10
        )

        response.raise_for_status()
        return True, None

    except requests.RequestException as error:
        return False, str(error)


# =========================
# PAGE CONNEXION
# =========================

if not st.session_state.token:

    st.markdown(
        '<div class="main-title">📝 NoteSpace</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Votre espace personnel de notes.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.subheader("Connexion")

        with st.form("login_form"):
            email = st.text_input("Adresse e-mail")
            password = st.text_input(
                "Mot de passe",
                type="password"
            )

            submitted = st.form_submit_button(
                "Se connecter",
                use_container_width=True
            )

        if submitted:
            if not email or not password:
                st.warning("Remplissez tous les champs.")
            else:
                with st.spinner("Connexion..."):
                    success, error = login(email, password)

                if success:
                    st.success("Connexion réussie !")
                    st.rerun()
                else:
                    st.error("Connexion impossible.")
                    st.code(error)

        st.caption("Connectez-vous avec votre compte NoteSpace.")


# =========================
# ESPACE CONNECTE
# =========================

else:

    notes, error = load_notes()

    # SIDEBAR
    with st.sidebar:
        st.markdown("## 📝 NoteSpace")
        st.caption("Your ideas, your space.")
        st.divider()

        st.success("Utilisateur connecté")
        st.caption(st.session_state.username)

        page = st.radio(
            "NAVIGATION",
            [
                "Tableau de bord",
                "Toutes les notes",
                "Nouvelle note",
                "À propos"
            ]
        )

        st.divider()

        if st.button("Se déconnecter", use_container_width=True):
            logout()

        st.caption("NoteSpace Dashboard")
        st.caption("Version 1.0")

    # HEADER
    st.markdown(
        '<div class="main-title">Bienvenue sur NoteSpace </div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">Gérez et organisez vos idées.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # GESTION ERREURS
    if error:

        st.error("Impossible de récupérer les notes.")

        if "Session expirée" in error:
            st.warning("Veuillez vous reconnecter.")
            if st.button("Retour à la connexion"):
                logout()
        else:
            st.code(error)

    else:

        total = len(notes)

        categories = set(
            note.get("category") or "Personnel"
            for note in notes
        )

        # =========================
        # TABLEAU DE BORD
        # =========================

        if page == "Tableau de bord":

            st.subheader("Vue générale")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total des notes", total)

            with col2:
                st.metric("Catégories", len(categories))

            with col3:
                st.metric("État", "Actif")

            st.divider()
            st.subheader("Notes récentes")

            if notes:
                for note in notes[:5]:
                    with st.container(border=True):
                        st.markdown(
                            f"### {note.get('title', 'Sans titre')}"
                        )
                        st.write(note.get("content", ""))
                        st.caption(
                            f" {note.get('category') or 'Personnel'}"
                        )
            else:
                st.info("Aucune note pour le moment.")

        # =========================
        # TOUTES LES NOTES
        # =========================

        elif page == "Toutes les notes":

            st.subheader("📚 Toutes mes notes")

            search = st.text_input(
                "🔍 Rechercher une note",
                placeholder="Titre ou contenu..."
            )

            filtered_notes = [
                note for note in notes
                if search.lower() in (
                    note.get("title", "") + " " +
                    note.get("content", "")
                ).lower()
            ]

            st.caption(
                f"{len(filtered_notes)} note(s) trouvée(s)"
            )

            for note in filtered_notes:

                note_id = note["id"]
                title = note.get("title") or "Sans titre"
                content = note.get("content") or ""
                category = note.get("category") or "Personnel"

                with st.expander(f"📝 {title}"):

                    st.write(content)
                    st.caption(f"Catégorie : {category}")

                    st.divider()

                    st.markdown("**Modifier cette note**")

                    with st.form(f"edit_form_{note_id}"):

                        new_title = st.text_input(
                            "Titre",
                            value=title,
                            key=f"title_{note_id}"
                        )

                        new_category = st.text_input(
                            "Catégorie",
                            value=category,
                            key=f"category_{note_id}"
                        )

                        new_content = st.text_area(
                            "Contenu",
                            value=content,
                            height=160,
                            key=f"content_{note_id}"
                        )

                        submitted = st.form_submit_button(
                            "Enregistrer les modifications",
                            use_container_width=True
                        )

                    if submitted:
                        if not new_title.strip():
                            st.warning("Le titre est obligatoire.")
                        else:
                            success, message = update_note(
                                note_id,
                                new_title.strip(),
                                new_content,
                                new_category.strip() or "Personnel"
                            )

                            if success:
                                st.success("Note modifiée !")
                                st.rerun()
                            else:
                                st.error("Modification impossible.")
                                st.code(message)

                    st.divider()

                    confirm_delete = st.checkbox(
                        "Je confirme vouloir supprimer cette note",
                        key=f"confirm_{note_id}"
                    )

                    if st.button(
                        "🗑️ Supprimer cette note",
                        key=f"delete_{note_id}",
                        disabled=not confirm_delete
                    ):
                        success, message = delete_note(note_id)

                        if success:
                            st.success("Note supprimée !")
                            st.rerun()
                        else:
                            st.error("Suppression impossible.")
                            st.code(message)

            if not filtered_notes:
                st.info("Aucune note trouvée.")

        # =========================
        # CREER UNE NOTE
        # =========================

        elif page == "Nouvelle note":

            st.subheader(" Créer une nouvelle note")

            with st.form("create_note_form"):

                title = st.text_input(
                    "Titre de la note",
                    placeholder="Exemple : Mon projet"
                )

                category = st.selectbox(
                    "Catégorie",
                    [
                        "Personnel",
                        "Travail",
                        "Études",
                        "Projets",
                        "Autres"
                    ]
                )

                content = st.text_area(
                    "Contenu",
                    placeholder="Écrivez votre note ici...",
                    height=250
                )

                submitted = st.form_submit_button(
                    "💾 Enregistrer la note",
                    use_container_width=True
                )

            if submitted:

                if not title.strip():
                    st.warning("Veuillez saisir un titre.")
                else:
                    success, message = create_note(
                        title.strip(),
                        content,
                        category
                    )

                    if success:
                        st.success("Votre note a été créée !")
                        st.rerun()
                    else:
                        st.error("Impossible de créer la note.")
                        st.code(message)

        # =========================
        # A PROPOS
        # =========================

        elif page == "À propos":

            st.subheader("À propos de NoteSpace")

            st.write("""
            NoteSpace est une application de prise de notes
            développée avec Python.

            **Technologies :**
            - Python et Kivy
            - FastAPI
            - MySQL
            - Streamlit
            - Tornado

            **Fonctionnalités :**
            - Authentification des utilisateurs
            - Création de notes
            - Consultation des notes
            - Modification des notes
            - Suppression des notes
            - Recherche de notes
            """)

        st.divider()

        if st.button(" Actualiser les données"):
            st.rerun()

        st.caption(
            f"NoteSpace © {datetime.now().year} | Dashboard"
        )
