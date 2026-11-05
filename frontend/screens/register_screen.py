from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp, sp

from frontend.services.api import (
    inscrire_utilisateur,
    connecter_utilisateur,
    obtenir_profil
)

WHITE = (0.95, 0.96, 1, 1)
ACCENT = (0.35, 0.48, 0.95, 1)


class RegisterScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(35), dp(25)],
            spacing=dp(12),
            size_hint=(None, None),
            width=dp(420),
            height=dp(620),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        layout.add_widget(Label(
            text="[b]Créer un compte[/b]",
            markup=True,
            font_size=sp(28),
            color=ACCENT,
            size_hint_y=None,
            height=dp(55)
        ))

        self.username = self.champ(layout, "Nom d'utilisateur")
        self.email = self.champ(layout, "Adresse email")
        self.password = self.champ(
            layout, "Mot de passe", password=True
        )
        self.confirm_password = self.champ(
            layout, "Confirmer le mot de passe", password=True
        )

        self.register_button = Button(
            text="Créer mon compte",
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=ACCENT,
            color=WHITE
        )
        self.register_button.bind(on_release=self.inscrire)
        layout.add_widget(self.register_button)

        back_button = Button(
            text="Retour à la connexion",
            size_hint_y=None,
            height=dp(45),
            background_normal="",
            background_color=(0.13, 0.16, 0.23, 1),
            color=WHITE
        )
        back_button.bind(
            on_release=lambda *_: setattr(
                self.manager, "current", "login"
            )
        )
        layout.add_widget(back_button)

        self.message = Label(
            text="",
            color=(1, 0.4, 0.4, 1),
            font_size=sp(12),
            size_hint_y=None,
            height=dp(45)
        )
        layout.add_widget(self.message)

        self.add_widget(layout)

    def champ(self, layout, indication, password=False):
        layout.add_widget(Label(
            text=indication,
            color=WHITE,
            halign="left",
            size_hint_y=None,
            height=dp(25)
        ))

        champ = TextInput(
            hint_text=indication,
            password=password,
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            padding=[dp(12), dp(10)],
            background_normal="",
            background_active="",
            background_color=(0.13, 0.16, 0.23, 1),
            foreground_color=WHITE
        )
        layout.add_widget(champ)
        return champ

    def inscrire(self, instance):
        username = self.username.text.strip()
        email = self.email.text.strip()
        password = self.password.text
        confirmation = self.confirm_password.text

        if not all([username, email, password, confirmation]):
            self.message.text = "Veuillez remplir tous les champs."
            return

        if len(username) < 3:
            self.message.text = "Nom d'utilisateur : 3 caractères minimum."
            return

        if password != confirmation:
            self.message.text = "Les mots de passe ne correspondent pas."
            return

        if len(password) < 8:
            self.message.text = "8 caractères minimum pour le mot de passe."
            return

        self.register_button.disabled = True
        self.register_button.text = "Création en cours..."
        self.message.text = ""

        succes, resultat = inscrire_utilisateur(
            username, email, password
        )

        if not succes:
            self.register_button.disabled = False
            self.register_button.text = "Créer mon compte"
            self.message.text = str(resultat)
            return

        # Connexion automatique après inscription.
        succes_login, resultat_login = connecter_utilisateur(
            email, password
        )

        self.register_button.disabled = False
        self.register_button.text = "Créer mon compte"

        if not succes_login:
            self.message.text = (
                "Compte créé. Connectez-vous depuis l'écran de connexion."
            )
            self.manager.current = "login"
            return

        token = resultat_login.get("access_token")

        if not token:
            self.message.text = (
                "Compte créé, mais aucun token reçu. Connectez-vous."
            )
            self.manager.current = "login"
            return

        app = App.get_running_app()
        app.access_token = token

        profil_ok, profil = obtenir_profil(token)
        app.current_user = profil if profil_ok else None

        self.message.color = (0.3, 0.9, 0.5, 1)
        self.message.text = "Compte créé avec succès."

        self.manager.current = "home"
