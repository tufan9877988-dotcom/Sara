from datetime import datetime

from kivy.app import App
from kivy.animation import Animation
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, RoundedRectangle, Triangle
from kivy.core.window import Window


Window.clearcolor = (0.055, 0.045, 0.13, 1)


PURPLE = (0.48, 0.30, 0.95, 1)
CARD = (0.13, 0.11, 0.25, 1)
WHITE = (0.96, 0.94, 1, 1)
MUTED = (0.72, 0.68, 0.85, 1)


class AnimeAvatar(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw_avatar, size=self.draw_avatar)
        self.draw_avatar()

        anim = (
            Animation(opacity=0.78, duration=1.0)
            + Animation(opacity=1, duration=1.0)
        )
        anim.repeat = True
        anim.start(self)

    def draw_avatar(self, *args):
        self.canvas.clear()

        x, y = self.pos
        w, h = self.size

        cx = x + w / 2
        cy = y + h / 2
        unit = min(w, h)

        with self.canvas:
            # Purple glowing background
            Color(0.38, 0.22, 0.85, 0.20)
            Ellipse(
                pos=(cx-unit*.49, cy-unit*.49),
                size=(unit*.98, unit*.98)
            )

            Color(0.55, 0.34, 1, 0.35)
            Line = None
            Ellipse(
                pos=(cx-unit*.43, cy-unit*.43),
                size=(unit*.86, unit*.86)
            )

            # Hair behind face
            Color(0.13, 0.09, 0.32, 1)
            Ellipse(
                pos=(cx-unit*.34, cy-unit*.28),
                size=(unit*.68, unit*.78)
            )

            # Shoulders and dress
            Color(0.40, 0.23, 0.90, 1)
            RoundedRectangle(
                pos=(cx-unit*.31, cy-unit*.48),
                size=(unit*.62, unit*.35),
                radius=[(unit*.14, unit*.14)]
            )

            # Face
            Color(1.0, 0.77, 0.72, 1)
            Ellipse(
                pos=(cx-unit*.235, cy-unit*.18),
                size=(unit*.47, unit*.55)
            )

            # Hair top
            Color(0.16, 0.10, 0.39, 1)
            Ellipse(
                pos=(cx-unit*.29, cy+unit*.04),
                size=(unit*.58, unit*.35)
            )

            # Hair fringe
            Color(0.22, 0.13, 0.52, 1)
            Triangle(points=[
                cx-unit*.26, cy+unit*.17,
                cx-unit*.03, cy+unit*.29,
                cx-unit*.09, cy+unit*.02
            ])
            Triangle(points=[
                cx-unit*.03, cy+unit*.22,
                cx+unit*.27, cy+unit*.16,
                cx+unit*.10, cy-unit*.02
            ])

            # Eyes
            Color(0.15, 0.10, 0.35, 1)
            Ellipse(
                pos=(cx-unit*.15, cy-unit*.015),
                size=(unit*.085, unit*.12)
            )
            Ellipse(
                pos=(cx+unit*.065, cy-unit*.015),
                size=(unit*.085, unit*.12)
            )

            # Eye highlights
            Color(1, 1, 1, 1)
            Ellipse(
                pos=(cx-unit*.13, cy+unit*.045),
                size=(unit*.025, unit*.03)
            )
            Ellipse(
                pos=(cx+unit*.085, cy+unit*.045),
                size=(unit*.025, unit*.03)
            )

            # Smile
            Color(0.75, 0.25, 0.43, 1)
            Ellipse(
                pos=(cx-unit*.035, cy-unit*.13),
                size=(unit*.07, unit*.025)
            )


class SARAApp(App):

    def build(self):
        self.title = "SARA AI"

        root = BoxLayout(
            orientation="vertical",
            padding=[dp(14), dp(8), dp(14), dp(8)],
            spacing=dp(8)
        )

        # HEADER
        header = BoxLayout(
            size_hint_y=None,
            height=dp(42)
        )

        header.add_widget(Label(
            text="[b]S A R A[/b] [color=#A58BFF]AI[/color]",
            markup=True,
            font_size=sp(23),
            color=WHITE,
            halign="left"
        ))

        header.add_widget(Label(
            text="✦",
            font_size=sp(27),
            color=(0.75, 0.62, 1, 1),
            size_hint_x=0.18
        ))

        root.add_widget(header)

        # SCROLLABLE DASHBOARD
        scroll = ScrollView(
            do_scroll_x=False,
            bar_width=dp(3)
        )

        content = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            padding=[0, dp(5), 0, dp(8)]
        )
        content.bind(minimum_height=content.setter("height"))

        # ANIME AVATAR
        avatar_area = AnchorLayout(
            size_hint_y=None,
            height=dp(165),
            anchor_x="center",
            anchor_y="center"
        )

        self.avatar = AnimeAvatar(
            size_hint=(None, None),
            size=(dp(155), dp(155))
        )

        avatar_area.add_widget(self.avatar)
        content.add_widget(avatar_area)

        # GREETING
        content.add_widget(Label(
            text="[b]Hello, I'm SARA![/b]",
            markup=True,
            font_size=sp(23),
            color=WHITE,
            size_hint_y=None,
            height=dp(35)
        ))

        content.add_widget(Label(
            text="Namaste! Aaj main aapki kya madad kar sakti hoon?",
            font_size=sp(12),
            color=MUTED,
            size_hint_y=None,
            height=dp(28)
        ))

        # QUICK ACTION TITLE
        content.add_widget(Label(
            text="[b]QUICK ACTIONS[/b]",
            markup=True,
            color=(0.75, 0.66, 1, 1),
            font_size=sp(14),
            halign="left",
            size_hint_y=None,
            height=dp(27)
        ))

        # QUICK ACTION TILES
        actions = GridLayout(
            cols=2,
            spacing=dp(10),
            size_hint_y=None,
            height=dp(140)
        )

        action_data = [
            ("♫", "Music"),
            ("✎", "Study"),
            ("♡", "Vent"),
            ("▣", "Photo")
        ]

        for symbol, name in action_data:
            btn = Button(
                text=f"[b]{symbol}[/b]\n{name}",
                markup=True,
                font_size=sp(17),
                color=WHITE,
                background_normal="",
                background_color=CARD,
                size_hint_y=None,
                height=dp(65)
            )
            btn.bind(
                on_release=lambda instance, n=name:
                self.show_message(n + " selected")
            )
            actions.add_widget(btn)

        content.add_widget(actions)

        # WIDGET TITLE
        content.add_widget(Label(
            text="[b]YOUR DAILY SPACE[/b]",
            markup=True,
            color=(0.75, 0.66, 1, 1),
            font_size=sp(14),
            halign="left",
            size_hint_y=None,
            height=dp(25)
        ))

        # WEATHER DATE MOOD
        info = GridLayout(
            cols=3,
            spacing=dp(7),
            size_hint_y=None,
            height=dp(88)
        )

        today = datetime.now().strftime("%d %b")

        info_items = [
            ("☁", "Weather", "Update later"),
            ("▦", "Date", today),
            ("☺", "Mood", "Feeling good?")
        ]

        for symbol, title, value in info_items:
            card = BoxLayout(
                orientation="vertical",
                padding=dp(5),
                spacing=dp(3)
            )

            with card.canvas.before:
                Color(*CARD)
                card_bg = RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[dp(12)]
                )

            card.bind(
                pos=lambda obj, val: setattr(card_bg, "pos", obj.pos),
                size=lambda obj, val: setattr(card_bg, "size", obj.size)
            )

            card.add_widget(Label(
                text=symbol,
                color=(0.73, 0.60, 1, 1),
                font_size=sp(21)
            ))

            card.add_widget(Label(
                text=f"[b]{title}[/b]",
                markup=True,
                color=WHITE,
                font_size=sp(11)
            ))

            card.add_widget(Label(
                text=value,
                color=MUTED,
                font_size=sp(9)
            ))

            info.add_widget(card)

        content.add_widget(info)

        # STATUS
        self.status = Label(
            text="SARA is ready for you ✨",
            color=(0.75, 0.68, 1, 1),
            font_size=sp(12),
            size_hint_y=None,
            height=dp(30)
        )

        content.add_widget(self.status)

        scroll.add_widget(content)
        root.add_widget(scroll)

        # BOTTOM NAVIGATION
        nav = BoxLayout(
            size_hint_y=None,
            height=dp(72),
            spacing=dp(3)
        )

        nav_items = [
            ("⌂", "Home"),
            ("◉", "Vision"),
        ]

        for symbol, name in nav_items:
            nav.add_widget(self.nav_button(symbol, name))

        # CENTRAL VOICE BUTTON
        self.mic_button = Button(
            text="🎙",
            font_size=sp(29),
            color=WHITE,
            background_normal="",
            background_color=PURPLE,
            size_hint_x=1.25
        )

        self.mic_button.bind(on_release=self.voice_action)
        nav.add_widget(self.mic_button)

        pulse = (
            Animation(
                background_color=(0.65, 0.35, 1, 1),
                duration=0.8
            )
            + Animation(
                background_color=PURPLE,
                duration=0.8
            )
        )
        pulse.repeat = True
        pulse.start(self.mic_button)

        nav.add_widget(self.nav_button("▣", "Memory"))
        nav.add_widget(self.nav_button("⚙", "Settings"))

        root.add_widget(nav)

        return root

    def nav_button(self, symbol, name):
        btn = Button(
            text=f"{symbol}\n{name}",
            font_size=sp(12),
            color=MUTED,
            background_normal="",
            background_color=(0.08, 0.06, 0.17, 1)
        )

        btn.bind(
            on_release=lambda instance:
            self.show_message(name + " section selected")
        )

        return btn

    def show_message(self, message):
        self.status.text = message

    def voice_action(self, instance):
        self.status.text = "Voice feature will be connected next! 🎙"


if __name__ == "__main__":
    SARAApp().run()
