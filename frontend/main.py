from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from frontend.screens.login_screen import LoginScreen
from frontend.screens.register_screen import RegisterScreen
from frontend.screens.home_screen import HomeScreen


class NoteSpaceApp(App):

    def build(self):
        self.title = "NoteSpace"

        Window.size = (1100, 720)
        Window.minimum_width = 800
        Window.minimum_height = 600
        Window.clearcolor = (0.055, 0.075, 0.12, 1)

        gestionnaire = ScreenManager(
            transition=FadeTransition(duration=0.2)
        )

        gestionnaire.add_widget(
            LoginScreen(name="login")
        )
        gestionnaire.add_widget(
            RegisterScreen(name="register")
        )
        gestionnaire.add_widget(
            HomeScreen(name="home")
        )

        gestionnaire.current = "login"

        return gestionnaire


if __name__ == "__main__":
    NoteSpaceApp().run()
