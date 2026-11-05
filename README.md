# 📝 NoteSpace

**NoteSpace** est une application de prise de notes développée avec Python. Elle permet de créer, modifier, supprimer, rechercher et organiser des notes dans une interface moderne et intuitive.

## 🛠️ Technologies utilisées

- Python 3.13
- Kivy 2.3.1
- FastAPI
- MySQL
- Git et GitHub

## ✨ Fonctionnalités

- Création, modification et suppression de notes.
- Recherche et organisation des notes.
- Mise en forme du texte.
- Interface graphique moderne.
- Stockage des données avec MySQL.
- Communication avec une API REST.

## 📋 Étapes de réalisation

1. Préparation de l'environnement sur Kali Linux.
2. Création de l'environnement virtuel Python.
3. Installation et configuration de Kivy.
4. Création de la structure du projet.
5. Développement de l'interface graphique avec Kivy.
6. Développement du backend avec FastAPI.
7. Configuration de la base de données MySQL.
8. Intégration du frontend et du backend.
9. Tests et corrections des erreurs.

## 📦 Prérequis

- Kali Linux ou Linux compatible.
- Python 3.13 ou supérieur.
- pip et venv.
- Git.
- MySQL Server.

## ⚙️ Installation

**1. Creer  le projet**

```bash
mkdir NoteSpace
cd NoteSpace
```

**2. Créer et activer l'environnement virtuel**

```bash
source "$HOME/Framwork KIVY/kivy_venv/bin/activate"
```

**3. Installer les dépendances**

```bash
pip install -r requirements.txt
```

## 🚀 Lancement

**Backend :**

```bash
cd backend
uvicorn main:app --reload
```

**Frontend :**

```bash
cd NoteSpace
source "$HOME/Framwork KIVY/kivy_venv/bin/activate"
python frontend/main.py
```

---

**NoteSpace – Your ideas, your space.**
