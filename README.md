# **NoteSpace**  
**NoteSpace** est une application de prise de notes développée avec Python. Elle permet de créer, modifier, supprimer, rechercher et organiser des notes grâce à une interface moderne et intuitive.  
   
**NoteSpace – Your ideas, your space.**  
## **Technologies utilisées**  
| | | |  
|-|-|-|  
| **Technologie** | **Utilisation** | **Documentation officielle** |   
| Python 3.13 | Langage principal | [Documentation](https://docs.python.org/3.13/ "https://docs.python.org/3.13/") |   
| Kivy 2.3.1 | Interface graphique | [Documentation](https://kivy.org/doc/stable-2.3.1/ "https://kivy.org/doc/stable-2.3.1/") |   
| FastAPI | API REST et backend | [Documentation](https://fastapi.tiangolo.com/ "https://fastapi.tiangolo.com/") |   
| MySQL / MariaDB | Base de données | [MySQL](https://dev.mysql.com/doc/ "https://dev.mysql.com/doc/") · [MariaDB](https://mariadb.com/docs/ "https://mariadb.com/docs/") |   
| SQLAlchemy | ORM et gestion des données | [Documentation](https://docs.sqlalchemy.org/en/20/ "https://docs.sqlalchemy.org/en/20/") |   
| JWT | Authentification | [PyJWT](https://pyjwt.readthedocs.io/en/stable/ "https://pyjwt.readthedocs.io/en/stable/") |   
| Streamlit | Tableau de bord | [Documentation](https://docs.streamlit.io/ "https://docs.streamlit.io/") |   
| Tornado | Serveur temps réel | [Documentation](https://www.tornadoweb.org/en/stable/ "https://www.tornadoweb.org/en/stable/") |   
| WebSocket | Communication temps réel | [RFC 6455](https://www.rfc-editor.org/rfc/rfc6455 "https://www.rfc-editor.org/rfc/rfc6455") |   
| Git / GitHub | Gestion de versions | [Git](https://git-scm.com/doc/ "https://git-scm.com/doc/") · [GitHub](https://docs.github.com/ "https://docs.github.com/") |   
## **✨ Fonctionnalités principales**  
- Création, modification et suppression des notes.  
- Recherche et gestion des favoris.  
- Inscription et connexion sécurisées avec JWT.  
- Interface graphique avec Kivy.  
- Tableau de bord avec Streamlit.  
- Notifications en temps réel avec Tornado et WebSocket.  
## **🏗️ Architecture du projet**  
NoteSpace/  
│  
├── backend/       # API FastAPI et base de données  
├── frontend/      # Interface graphique Kivy  
├── dashboard/     # Tableau de bord Streamlit  
├── realtime/      # Serveur Tornado et WebSocket  
├── .streamlit/    # Configuration Streamlit  
│  
├── requirements.txt  
├── README.md  
└── .gitignore  
## **Prérequis**  
- Kali Linux   
- Python 3.13  
- MySQL ou MariaDB  
- Git  
- pip et venv  
## **⚙️ Installation**  
**1. Cloner le projet**  
git clone https://github.com/cathysahy/Notespace-bloc-note-.git  
cd NoteSpace  
**2. Activer l'environnement virtuel**  
source "$HOME/Framwork KIVY/kivy_venv/bin/activate"  
**3. Installer les dépendances**  
pip install -r requirements.txt  
**4. Configurer la base de données**  
Créer la base de données notespace_db et configurer les variables d'environnement dans le fichier .env.  
## **🚀 Lancement**  
Lancer chaque service dans un terminal séparé.  
| | |  
|-|-|  
| **Service** | **Commande** |   
| Backend FastAPI | uvicorn backend.main:app --reload |   
| Application Kivy | python frontend/main.py |   
| Dashboard Streamlit | streamlit run dashboard/app.py |   
| Serveur Tornado | python realtime/server.py |   
   
**Accès à l'API :** [http://127.0.0.1:8000](http://127.0.0.1:8000/ "http://127.0.0.1:8000/")  
**Documentation interactive :** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs "http://127.0.0.1:8000/docs")  
**Dashboard :** [http://localhost:8501](http://localhost:8501/ "http://localhost:8501/")  
**Serveur temps réel :** [http://localhost:8765](http://localhost:8765/ "http://localhost:8765/")  
   
   
**NoteSpace – Your ideas, your space.**  
   
