from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp

from frontend.services.api import (
    connecter_utilisateur,
    obtenir_profil
)

BACKGROUND = (0.055, 0.075, 0.12, 1)
ACCENT = (0.35, 0.48, 0.95, 1)
WHITE = (0.95, 0.96, 1, 1)
MUTED = (0.65, 0.69, 0.78, 1)


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=[dp(35), dp(30)],
            spacing=dp(15),
            size_hint=(None, None),
            width=dp(420),
            height=dp(560),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        layout.add_widget(Label(
            text="[b]NoteSpace[/b]",
            markup=True,
            font_size=sp(34),
            color=ACCENT,
            size_hint_y=None,
            height=dp(65)
        ))

        layout.add_widget(Label(
            text="Bienvenue dans votre espace de notes",
            font_size=sp(14),
            color=MUTED,
            size_hint_y=None,
            height=dp(35)
        ))

        layout.add_widget(Widget(size_hint_y=None, height=dp(15)))

        layout.add_widget(Label(
            text="Adresse email",
            color=WHITE,
            halign="left",
            size_hint_y=None,
            height=dp(28)
        ))

        self.email = TextInput(
            hint_text="exemple@email.com",
            multiline=False,
            size_hint_y=None,
            height=dp(48),
            padding=[dp(12), dp(12)],
            background_normal="",
            background_active="",
            background_color=(0.13, 0.16, 0.23, 1),
            foreground_color=WHITE,
            cursor_color=ACCENT
        )
        layout.add_widget(self.email)

        layout.add_widget(Label(
            text="Mot de passe",
            color=WHITE,
            halign="left",
            size_hint_y=None,
            height=dp(28)
        ))

        self.password = TextInput(
            hint_text="Votre mot de passe",
            password=True,
            multiline=False,
            size_hint_y=None,
            height=dp(48),
            padding=[dp(12), dp(12)],
            background_normal="",
            background_active="",
            background_color=(0.13, 0.16, 0.23, 1),
            foreground_color=WHITE,
            cursor_color=ACCENT
        )
        layout.add_widget(self.password)

        layout.add_widget(Widget(size_hint_y=None, height=dp(10)))

        self.login_button = Button(
            text="Se connecter",
            size_hint_y=None,
            height=dp(50),
            background_normal="",
            background_color=ACCENT,
            color=WHITE
        )
        self.login_button.bind(on_release=self.connecter)
        layout.add_widget(self.login_button)

        register_button = Button(
            text="Créer un compte",
            size_hint_y=None,
            height=dp(45),
            background_normal="",
            background_color=(0.13, 0.16, 0.23, 1),
            color=WHITE
        )
        register_button.bind(
            on_release=lambda *_: setattr(
                self.manager, "current", "register"
            )
        )
        layout.add_widget(register_button)

        self.message = Label(
            text="",
            color=(1, 0.4, 0.4, 1),
            font_size=sp(12),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.message)

        self.add_widget(layout)

    def connecter(self, instance):
        email = self.email.text.strip()
        password = self.password.text

        if not email or not password:
            self.message.text = "Veuillez remplir tous les champs."
            return

        self.login_button.disabled = True
        self.login_button.text = "Connexion en cours..."
        self.message.text = ""

        succes, resultat = connecter_utilisateur(email, password)

        self.login_button.disabled = False
        self.login_button.text = "Se connecter"

        if not succes:
            self.message.text = str(resultat)
            return

        token = resultat.get("access_token")

        if not token:
            self.message.text = "Le serveur n'a pas fourni de token."
            return

        app = App.get_running_app()
        app.access_token = token

        profil_ok, profil = obtenir_profil(token)

        app.current_user = profil if profil_ok else None

        self.message.color = (0.3, 0.9, 0.5, 1)
        self.message.text = "Connexion réussie."

        self.manager.current = "home"
