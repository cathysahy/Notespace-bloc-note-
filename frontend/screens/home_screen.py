import re

from kivy.app import App
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

from frontend.services.api import (
    obtenir_notes,
    creer_note,
    modifier_note,
    supprimer_note
)


# ==================================================
# COULEURS
# ==================================================

DARK = (0.12, 0.12, 0.12, 1)
DARK_BUTTON = (0.16, 0.16, 0.16, 1)

BACKGROUND = (0.98, 0.97, 0.95, 1)
WHITE = (1, 1, 1, 1)

TEXT = (0.12, 0.12, 0.12, 1)
MUTED = (0.55, 0.55, 0.55, 1)

ORANGE = (0.80, 0.42, 0.30, 1)
GREEN = (0.25, 0.62, 0.35, 1)
GOLD = (0.80, 0.58, 0.18, 1)
RED = (0.78, 0.25, 0.25, 1)


class HomeScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.notes = []
        self.current_note = None
        self.current_filter = "Toutes"
        self.favorite_ids = set()
        self.editor_mode = False

        self.build_interface()

    # ==================================================
    # FONDS
    # ==================================================

    def set_background(self, widget, color):

        with widget.canvas.before:
            Color(*color)
            widget.bg_rectangle = Rectangle(
                pos=widget.pos,
                size=widget.size
            )

        widget.bind(
            pos=lambda instance, value: setattr(
                instance.bg_rectangle, "pos", value
            ),
            size=lambda instance, value: setattr(
                instance.bg_rectangle, "size", value
            )
        )

    # ==================================================
    # LABEL
    # ==================================================

    def make_label(
        self,
        text,
        size=14,
        color=TEXT,
        bold=False,
        height=None
    ):

        label = Label(
            text=text,
            font_size=sp(size),
            color=color,
            bold=bold,
            halign="left",
            valign="middle"
        )

        if height:
            label.size_hint_y = None
            label.height = dp(height)

        label.bind(
            size=lambda instance, value:
            setattr(instance, "text_size", (value[0], None))
        )

        return label

    # ==================================================
    # BOUTONS
    # ==================================================

    def make_button(
        self,
        text,
        callback,
        color=WHITE,
        text_color=TEXT,
        height=42
    ):

        button = Button(
            text=text,
            size_hint_y=None,
            height=dp(height),
            background_normal="",
            background_down="",
            background_color=color,
            color=text_color,
            font_size=sp(13)
        )

        button.bind(on_release=callback)

        return button

    # ==================================================
    # INTERFACE PRINCIPALE
    # ==================================================

    def build_interface(self):

        self.clear_widgets()

        root = BoxLayout(
            orientation="horizontal",
            spacing=0
        )

        self.set_background(root, BACKGROUND)

        # ==============================================
        # BARRE LATERALE
        # ==============================================

        sidebar = BoxLayout(
            orientation="vertical",
            size_hint_x=None,
            width=dp(245),
            padding=[dp(15), dp(20)],
            spacing=dp(12)
        )

        self.set_background(sidebar, DARK)

        logo = self.make_label(
            "◉  NoteSpace",
            24,
            WHITE,
            True,
            55
        )

        sidebar.add_widget(logo)

        sidebar.add_widget(
            self.make_button(
                "＋  Nouvelle note",
                self.nouvelle_note,
                ORANGE,
                WHITE,
                48
            )
        )

        sidebar.add_widget(
            self.make_label(
                "ESPACE",
                12,
                MUTED,
                True,
                35
            )
        )

        self.all_button = self.make_button(
            "▤  Toutes les notes",
            lambda *_: self.filtrer("Toutes"),
            DARK_BUTTON,
            WHITE
        )

        sidebar.add_widget(self.all_button)

        self.favorites_button = self.make_button(
            "☆  Favoris",
            lambda *_: self.filtrer("Favoris"),
            DARK_BUTTON,
            WHITE
        )

        sidebar.add_widget(self.favorites_button)

        sidebar.add_widget(Label())

        footer = self.make_label(
            "CN   Espace Créatif",
            13,
            WHITE,
            False,
            40
        )

        sidebar.add_widget(footer)

        # ==============================================
        # ESPACE PRINCIPAL
        # ==============================================

        self.main = BoxLayout(
            orientation="vertical",
            spacing=0
        )

        self.set_background(self.main, BACKGROUND)

        root.add_widget(sidebar)
        root.add_widget(self.main)

        self.add_widget(root)

        self.afficher_galerie()

    # ==================================================
    # BARRE SUPERIEURE
    # ==================================================

    def construire_topbar(self):

        topbar = BoxLayout(
            size_hint_y=None,
            height=dp(58),
            padding=[dp(25), dp(8)],
            spacing=dp(15)
        )

        self.set_background(topbar, WHITE)

        topbar.add_widget(
            self.make_label(
                "Notespace   ›   Galerie des carnets & notes",
                15,
                TEXT,
                True
            )
        )

        self.count_label = self.make_label(
            "0 carnets actifs",
            12,
            MUTED
        )

        self.count_label.size_hint_x = None
        self.count_label.width = dp(125)

        topbar.add_widget(self.count_label)

        return topbar

    # ==================================================
    # GALERIE
    # ==================================================

    def afficher_galerie(self):

        self.editor_mode = False
        self.main.clear_widgets()

        self.main.add_widget(
            self.construire_topbar()
        )

        # BARRE DES FILTRES

        filter_row = BoxLayout(
            size_hint_y=None,
            height=dp(65),
            padding=[dp(20), dp(10)],
            spacing=dp(9)
        )

        self.set_background(filter_row, BACKGROUND)

        filters = [
            ("Toutes les notes", "Toutes", DARK),
            ("● Travail", "Travail", ORANGE),
            ("● Personnel", "Personnel", GREEN),
            ("★ Favoris", "Favoris", GOLD)
        ]

        for title, value, color in filters:

            button = Button(
                text=title,
                size_hint_x=None,
                width=dp(125),
                background_normal="",
                background_color=(
                    DARK if self.current_filter == value
                    else WHITE
                ),
                color=(
                    WHITE if self.current_filter == value
                    else TEXT
                ),
                font_size=sp(12)
            )

            button.bind(
                on_release=lambda instance, item=value:
                self.filtrer(item)
            )

            filter_row.add_widget(button)

        filter_row.add_widget(Label())

        self.search = TextInput(
            hint_text="⌕  Rechercher...",
            multiline=False,
            size_hint_x=None,
            width=dp(180),
            background_normal="",
            background_active="",
            background_color=WHITE,
            foreground_color=TEXT,
            cursor_color=ORANGE,
            padding=dp(10),
            font_size=sp(12)
        )

        self.search.bind(
            text=lambda *_: self.actualiser_liste()
        )

        filter_row.add_widget(self.search)

        self.main.add_widget(filter_row)

        # TITRE DE COLLECTION

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(85),
            padding=[dp(28), dp(8)]
        )

        header.add_widget(
            self.make_label(
                "Collection de carnets",
                23,
                TEXT,
                True
            )
        )

        header.add_widget(
            self.make_label(
                "Carnets reliés, recueils d'idées et notes d'écriture créative.",
                12,
                MUTED
            )
        )

        self.main.add_widget(header)

        # GRILLE DES NOTES

        scroll = ScrollView(
            do_scroll_x=False
        )

        self.note_list = GridLayout(
            cols=3,
            spacing=dp(18),
            padding=[dp(25), dp(10)],
            size_hint_y=None
        )

        self.note_list.bind(
            minimum_height=self.note_list.setter("height")
        )

        scroll.add_widget(self.note_list)

        self.main.add_widget(scroll)

        self.actualiser_liste()

    # ==================================================
    # COULEUR DE CATEGORIE
    # ==================================================

    def category_color(self, category):

        category = (category or "").lower()

        if "travail" in category:
            return ORANGE

        if "personnel" in category:
            return GREEN

        return GOLD

    # ==================================================
    # CARTE D'UNE NOTE
    # ==================================================

    def creer_carte(self, note):

        category = note.get("category") or "Général"

        title = note.get("title") or "Sans titre"

        content = note.get("content") or ""

        note_id = note.get("id")

        color = self.category_color(category)

        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(235),
            spacing=dp(7),
            padding=dp(14)
        )

        self.set_background(card, WHITE)

        # Bande colorée

        strip = BoxLayout(
            size_hint_y=None,
            height=dp(7)
        )

        self.set_background(strip, color)

        card.add_widget(strip)

        # Entête

        header = BoxLayout(
            size_hint_y=None,
            height=dp(30)
        )

        category_label = Label(
            text="● " + category.upper(),
            color=color,
            font_size=sp(10),
            bold=True,
            halign="left"
        )

        header.add_widget(category_label)

        favorite = Button(
            text="★" if note_id in self.favorite_ids else "☆",
            size_hint_x=None,
            width=dp(35),
            background_normal="",
            background_color=WHITE,
            color=GOLD if note_id in self.favorite_ids else MUTED,
            font_size=sp(19)
        )

        favorite.bind(
            on_release=lambda instance, item=note:
            self.basculer_favori_carte(item)
        )

        header.add_widget(favorite)

        card.add_widget(header)

        # Titre

        card.add_widget(
            self.make_label(
                title,
                17,
                TEXT,
                True,
                35
            )
        )

        # Aperçu

        preview = re.sub(
            r"!\[[^\]]*\]\([^)]+\)",
            "",
            content
        ).replace("\n", " ")

        if len(preview) > 125:
            preview = preview[:125] + "..."

        description = self.make_label(
            preview,
            11,
            MUTED
        )

        card.add_widget(description)

        card.add_widget(Label())

        # Pied de carte

        footer = BoxLayout(
            size_hint_y=None,
            height=dp(30)
        )

        words = len(content.split())

        footer.add_widget(
            self.make_label(
                "◷  Note",
                10,
                MUTED
            )
        )

        footer.add_widget(
            self.make_label(
                str(words) + " mots",
                10,
                MUTED
            )
        )

        card.add_widget(footer)

        # Ouverture

        open_button = Button(
            text="Ouvrir cette note",
            size_hint_y=None,
            height=dp(28),
            background_normal="",
            background_color=(0.95, 0.95, 0.95, 1),
            color=TEXT,
            font_size=sp(10)
        )

        open_button.bind(
            on_release=lambda instance:
            self.ouvrir_note(note)
        )

        card.add_widget(open_button)

        return card

    # ==================================================
    # ACTUALISATION DE LA GALERIE
    # ==================================================

    def actualiser_liste(self):

        if not hasattr(self, "note_list"):
            return

        self.note_list.clear_widgets()

        notes = self.notes

        if self.current_filter == "Favoris":

            notes = [
                note for note in notes
                if note.get("id") in self.favorite_ids
            ]

        elif self.current_filter in ("Travail", "Personnel"):

            notes = [
                note for note in notes
                if (note.get("category") or "").lower()
                == self.current_filter.lower()
            ]

        recherche = ""

        if hasattr(self, "search"):
            recherche = self.search.text.lower().strip()

        notes = [
            note for note in notes
            if recherche in (
                note.get("title", "") + " "
                + note.get("content", "") + " "
                + (note.get("category") or "")
            ).lower()
        ]

        self.count_label.text = (
            str(len(notes)) + " éléments"
        )

        for note in reversed(notes):

            self.note_list.add_widget(
                self.creer_carte(note)
            )

        # Carte nouvelle note

        new_card = Button(
            text="+\n\nNouveau carnet ou note\n\n"
                 "Créer un espace pour vos\n"
                 "réflexions, projets ou voyages.",
            size_hint_y=None,
            height=dp(235),
            background_normal="",
            background_color=(0.99, 0.99, 0.99, 1),
            color=MUTED,
            font_size=sp(14)
        )

        new_card.bind(
            on_release=self.nouvelle_note
        )

        self.note_list.add_widget(new_card)

    # ==================================================
    # FILTRES
    # ==================================================

    def filtrer(self, categorie):

        self.current_filter = categorie

        self.afficher_galerie()

    # ==================================================
    # CHARGEMENT DES NOTES
    # ==================================================

    def on_pre_enter(self, *args):

        self.charger_notes()

    def charger_notes(self):

        app = App.get_running_app()

        token = getattr(app, "access_token", None)

        if not token:
            return

        success, result = obtenir_notes(token)

        if success:

            self.notes = result

            if not self.editor_mode:
                self.actualiser_liste()

        else:

            print("Erreur chargement notes :", result)

    # ==================================================
    # EDITEUR
    # ==================================================

    def afficher_editeur(self):

        self.editor_mode = True
        self.main.clear_widgets()

        self.main.add_widget(
            self.construire_topbar()
        )

        editor = BoxLayout(
            orientation="vertical",
            padding=[dp(45), dp(25)],
            spacing=dp(15)
        )

        self.set_background(editor, WHITE)

        # Retour

        editor.add_widget(
            self.make_button(
                "← Retour à la galerie",
                lambda *_: self.afficher_galerie(),
                DARK_BUTTON,
                WHITE
            )
        )

        # Catégorie

        self.category = TextInput(
            hint_text="Catégorie : Travail, Personnel...",
            multiline=False,
            size_hint_y=None,
            height=dp(42),
            background_normal="",
            background_active="",
            background_color=BACKGROUND,
            foreground_color=ORANGE,
            padding=dp(12)
        )

        editor.add_widget(self.category)

        # Titre

        self.title_input = TextInput(
            hint_text="Titre de votre note",
            multiline=False,
            size_hint_y=None,
            height=dp(65),
            font_size=sp(25),
            background_normal="",
            background_active="",
            background_color=WHITE,
            foreground_color=TEXT,
            padding=dp(10)
        )

        editor.add_widget(self.title_input)

        # Contenu

        self.content_input = TextInput(
            hint_text="Commencez à écrire vos idées ici...",
            multiline=True,
            background_normal="",
            background_active="",
            background_color=WHITE,
            foreground_color=TEXT,
            font_size=sp(16),
            padding=dp(12)
        )

        editor.add_widget(self.content_input)

        # Actions

        actions = BoxLayout(
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10)
        )

        self.favorite_button = Button(
            text="☆ Favori",
            background_normal="",
            background_color=DARK_BUTTON,
            color=WHITE
        )

        self.favorite_button.bind(
            on_release=self.basculer_favori
        )

        actions.add_widget(self.favorite_button)

        actions.add_widget(Label())

        delete_button = Button(
            text="Supprimer",
            size_hint_x=None,
            width=dp(110),
            background_normal="",
            background_color=RED,
            color=WHITE
        )

        delete_button.bind(
            on_release=self.supprimer
        )

        actions.add_widget(delete_button)

        self.save_button = Button(
            text="Créer la note",
            size_hint_x=None,
            width=dp(140),
            background_normal="",
            background_color=ORANGE,
            color=WHITE
        )

        self.save_button.bind(
            on_release=self.enregistrer
        )

        actions.add_widget(self.save_button)

        editor.add_widget(actions)

        self.main.add_widget(editor)

    # ==================================================
    # NOUVELLE NOTE
    # ==================================================

    def nouvelle_note(self, instance=None):

        self.current_note = None

        self.afficher_editeur()

        self.title_input.text = ""
        self.content_input.text = ""
        self.category.text = ""

        self.favorite_button.text = "☆ Favori"
        self.save_button.text = "Créer la note"

    # ==================================================
    # OUVRIR UNE NOTE
    # ==================================================

    def ouvrir_note(self, note):

        self.current_note = note

        self.afficher_editeur()

        self.title_input.text = note.get("title", "")

        self.content_input.text = note.get("content", "")

        self.category.text = note.get("category") or ""

        note_id = note.get("id")

        self.favorite_button.text = (
            "★ Favori"
            if note_id in self.favorite_ids
            else "☆ Favori"
        )

        self.save_button.text = "Modifier la note"

    # ==================================================
    # ENREGISTRER
    # ==================================================

    def enregistrer(self, instance):

        title = self.title_input.text.strip()

        content = self.content_input.text.strip()

        category = self.category.text.strip() or "Général"

        if not title or not content:

            print("Le titre et le contenu sont obligatoires.")

            return

        app = App.get_running_app()

        token = getattr(app, "access_token", None)

        if not token:
            return

        self.save_button.disabled = True

        try:

            if self.current_note is None:

                success, result = creer_note(
                    token,
                    title,
                    content,
                    category
                )

            else:

                success, result = modifier_note(
                    token,
                    self.current_note["id"],
                    title,
                    content,
                    category
                )

            if success:

                self.charger_notes()

                self.current_note = result

                self.afficher_galerie()

            else:

                print("Erreur API :", result)

        finally:

            self.save_button.disabled = False

    # ==================================================
    # FAVORIS
    # ==================================================

    def basculer_favori(self, instance):

        if self.current_note is None:
            return

        note_id = self.current_note["id"]

        if note_id in self.favorite_ids:

            self.favorite_ids.remove(note_id)

            self.favorite_button.text = "☆ Favori"

        else:

            self.favorite_ids.add(note_id)

            self.favorite_button.text = "★ Favori"

    def basculer_favori_carte(self, note):

        note_id = note.get("id")

        if note_id in self.favorite_ids:

            self.favorite_ids.remove(note_id)

        else:

            self.favorite_ids.add(note_id)

        self.actualiser_liste()

    # ==================================================
    # SUPPRESSION
    # ==================================================

    def supprimer(self, instance):

        if self.current_note is None:
            return

        contenu = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        contenu.add_widget(
            Label(
                text="Voulez-vous vraiment supprimer cette note ?",
                color=TEXT
            )
        )

        boutons = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )

        popup = Popup(
            title="Confirmer la suppression",
            content=contenu,
            size_hint=(0.8, 0.3)
        )

        annuler = Button(text="Annuler")

        confirmer = Button(
            text="Supprimer",
            background_normal="",
            background_color=RED,
            color=WHITE
        )

        annuler.bind(
            on_release=popup.dismiss
        )

        confirmer.bind(
            on_release=lambda *_:
            self.confirmer_suppression(popup)
        )

        boutons.add_widget(annuler)
        boutons.add_widget(confirmer)

        contenu.add_widget(boutons)

        popup.open()

    def confirmer_suppression(self, popup):

        app = App.get_running_app()

        token = getattr(app, "access_token", None)

        if not token or not self.current_note:
            popup.dismiss()
            return

        note_id = self.current_note["id"]

        success, result = supprimer_note(
            token,
            note_id
        )

        popup.dismiss()

        if success:

            self.favorite_ids.discard(note_id)

            self.current_note = None

            self.charger_notes()

            self.afficher_galerie()

        else:

            print("Erreur suppression :", result)

    # ==================================================
    # DECONNEXION
    # ==================================================

    def deconnexion(self, instance):

        app = App.get_running_app()

        app.access_token = None

        app.current_user = None

        self.manager.current = "login"
