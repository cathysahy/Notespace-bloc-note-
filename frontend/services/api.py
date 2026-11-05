import requests

API_URL = "http://127.0.0.1:8000"


def inscrire_utilisateur(username, email, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "username": username,
                "email": email,
                "password": password
            },
            timeout=10
        )

        if response.status_code == 201:
            return True, response.json()

        try:
            message = response.json().get("detail", "Erreur inconnue")
        except ValueError:
            message = "Réponse invalide du serveur"

        return False, str(message)

    except requests.RequestException:
        return False, "Impossible de contacter le serveur FastAPI"


def connecter_utilisateur(email, password):
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
            return True, response.json()

        try:
            message = response.json().get(
                "detail", "Identifiants incorrects"
            )
        except ValueError:
            message = "Réponse invalide du serveur"

        return False, str(message)

    except requests.RequestException:
        return False, "Impossible de contacter le serveur FastAPI"


def obtenir_profil(token):
    try:
        response = requests.get(
            f"{API_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )

        if response.status_code == 200:
            return True, response.json()

        return False, "Session invalide ou expirée"

    except requests.RequestException:
        return False, "Impossible de contacter le serveur FastAPI"


def entetes_auth(token):
    return {"Authorization": f"Bearer {token}"}


def obtenir_notes(token):
    try:
        response = requests.get(
            f"{API_URL}/notes/",
            headers=entetes_auth(token),
            timeout=10
        )

        if response.status_code == 200:
            return True, response.json()

        return False, response.text

    except requests.RequestException as error:
        return False, str(error)


def creer_note(token, title, content, category):
    try:
        response = requests.post(
            f"{API_URL}/notes/",
            headers=entetes_auth(token),
            json={
                "title": title,
                "content": content,
                "category": category
            },
            timeout=10
        )

        if response.status_code == 201:
            return True, response.json()

        return False, response.text

    except requests.RequestException as error:
        return False, str(error)


def modifier_note(token, note_id, title, content, category):
    try:
        response = requests.put(
            f"{API_URL}/notes/{note_id}",
            headers=entetes_auth(token),
            json={
                "title": title,
                "content": content,
                "category": category
            },
            timeout=10
        )

        if response.status_code == 200:
            return True, response.json()

        return False, response.text

    except requests.RequestException as error:
        return False, str(error)


def supprimer_note(token, note_id):
    try:
        response = requests.delete(
            f"{API_URL}/notes/{note_id}",
            headers=entetes_auth(token),
            timeout=10
        )

        if response.status_code == 200:
            return True, response.json()

        return False, response.text

    except requests.RequestException as error:
        return False, str(error)
