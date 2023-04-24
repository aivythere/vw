from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
import dt
import bfont
import palette
import appconf
import elements


class CongratzScreen(MDScreen):

    def __init__(self, screen_manager):
        super(CongratzScreen, self).__init__()
        self.name = "Congratz"
        self.scr = screen_manager

        main_grid = MDGridLayout(cols=1, spacing=50, padding=[150, 400, 150, 500])
        self.pic = Image(source='images/congratz.png', allow_stretch=True)
        congratz_text = bfont.MSFont("Поздравляем!\nВклад открыт", style='Bold', halign='center')

        self.menu_button = MDCard(
            bfont.MSFont(
                text='В меню',
                size="25sp",
                style="Bold",
                halign='center'
            ),
            md_bg_color=palette.accent_yellow_rgba,
            radius=appconf.CARD_RADIUS,
            ripple_behavior=True,
            on_release=lambda *a: self.escapeScreen(mp=False),
            size_hint_x=.5

        )

        self.mypacks_button = MDCard(
            bfont.MSFont(
                text='Мои вклады',
                size="25sp",
                style="Bold",
                halign='center'
            ),
            md_bg_color=palette.blued_gray_main_rgba,
            radius=appconf.CARD_RADIUS,
            ripple_behavior=True,
            on_release=lambda *a: self.escapeScreen(mp=True),
            size_hint_x = .5
        )

        main_grid.add_widget(self.pic)
        main_grid.add_widget(congratz_text)
        main_grid.add_widget(self.mypacks_button)
        main_grid.add_widget(self.menu_button)

        self.add_widget(main_grid)


    def escapeScreen(self, mp=False, *args):
        if not mp:
            elements.change_screen(self.scr, "MainMenu", ts_dir='right')
        else:
            elements.change_screen(self.scr, "MyPacks", ts_dir='right')
        Clock.schedule_once(lambda *a: self.scr.remove_widget(self), 1)
