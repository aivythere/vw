from datetime import timedelta, datetime
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
import bfont
import palette
import appconf
import cache_manager

def change_screen(screen_manager, to_sc, ts_dir='left'):
    screen_manager.transition = appconf.DEFAULT_TRANSITION
    screen_manager.transition.direction = ts_dir
    screen_manager.current = to_sc


class TextCard(MDCard):
    def __init__(self, main_text: str, radius=appconf.CARD_RADIUS, sec_text=None):
        super().__init__()
        grid = MDGridLayout(cols=1, padding=50, spacing=10)
        self.md_bg_color = palette.blued_gray_main_rgba
        self.radius = radius
        self.main_text = bfont.MSFont(text=main_text, style="Bold", size="25sp")
        grid.add_widget(self.main_text)
        if sec_text:
            self.secondary_text = bfont.MSFont(text=sec_text, size="13sp")
            grid.add_widget(self.secondary_text)
        self.add_widget(grid)


class BetterMoneyTextInput(MDCard):
    def __init__(self, on_text_change, **kwargs):
        super(BetterMoneyTextInput, self).__init__(**kwargs)
        self.md_bg_color = palette.blued_gray_main_rgba
        self.padding = 20
        self.radius = 40
        grid = MDGridLayout(cols=2)
        input_text_card = MDCard(
            md_bg_color=(1, 1, 1, 1),
            radius=50,
            padding=[0, 0, 0, 20],
            size_hint_x=.6

        )
        opg = MDFloatLayout()

        self.text_field = MDTextField(
            font_size=sp(25),
            font_name="fonts/MS_Bold",
            text_color_focus=(0, 0, 0, 1),
            line_color_normal=(1, 1, 1, 1),
            line_color_focus=(1, 1, 1, 1),
            pos_hint={'center_y': .5, 'center_x': .45},
            size_hint_x=.7,
            cursor_color=(1, 1, 1, 1),
            input_filter='int'
        )
        opg.add_widget(self.text_field)
        input_text_card.add_widget(opg)
        self.text_field.bind(
            text=on_text_change
        )

        grid.add_widget(input_text_card)
        grid.add_widget(
                bfont.MSFont(
                text="₽", style='Bold', size='40sp', halign='center', valign='center',
                size_hint_x=.1, text_color=(0, 0, 0, 1), theme_text_color="Custom"
            )
        )
        self.add_widget(grid)


class ERRPopupFilling(MDBoxLayout):
    def __init__(self):
        super().__init__()
        self.size_hint_y = None
        self.height = dp(150)
        self.md_bg_color = (0, 0, 0, 0)
        self.ErrorCard_instance = self.ErrorCard()
        err_image = Image(source="images/error.png", allow_stretch=True,
                          size_hint=[.5, .5])
        err_caption = bfont.MSFont(
            text=f'[size=20sp][font=fonts/MS_Bold]Ошибка сети.[/font][/size]'
                 f'[size=15sp]\n\nПроверьте подключение к сети, либо узнайте статус серверов на {appconf.DOMAIN}',
            halign='center', valign='center')
        self.ErrorCard_instance.inner_grid.add_widget(err_image)
        self.ErrorCard_instance.inner_grid.add_widget(err_caption)
        self.add_widget(self.ErrorCard_instance)

    class ErrorCard(MDCard):
        def __init__(self):
            super().__init__()
            self.md_bg_color = (0, 0, 0, 0)
            self.inner_grid = MDGridLayout(cols=1, rows=2, spacing=50, size_hint_y=None, height=dp(150))
            self.padding = [50, 50, 50, 50]
            self.radius = 30
            self.size_hint = [.5, .5]
            self.add_widget(self.inner_grid)


class BetterTextInput(MDCard):
    def __init__(self, pic_filename, on_text_change=lambda *a: ..., placeholder='', input_filter=False, font_size=30,
                 **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = palette.blued_gray_main_rgba
        self.padding = 30
        self.radius = 40
        self.size_hint_y = .3
        self.placeholder_text = placeholder
        grid = MDGridLayout(cols=2, spacing=30)
        input_text_card = MDCard(
            md_bg_color=(1, 1, 1, 1),
            radius=50,
            padding=[0, 0, 0, 20],
            size_hint_x=.6,

        )
        opg = MDFloatLayout()

        self.text_field = MDTextField(
            font_size=sp(font_size),
            font_name="fonts/MS_Bold",
            text_color_focus=(0, 0, 0, 1),
            line_color_normal=(1, 1, 1, 1),
            line_color_focus=(1, 1, 1, 1),
            pos_hint={'center_y': .5, 'center_x': .45},
            size_hint_x=.7,
            text=placeholder,
        )
        if input_filter: self.text_field.input_filter = input_filter
        opg.add_widget(self.text_field)
        input_text_card.add_widget(opg)
        self.text_field.bind(
            text=on_text_change,
            focus=self.is_placeholder
        )

        grid.add_widget(input_text_card)
        grid.add_widget(
            Image(source=f'images/{pic_filename}', size_hint=[.07, .07], allow_stretch=True)
        )
        self.add_widget(grid)

    def is_placeholder(self, *args):
        if args[-1]:
            if self.text_field.text in appconf.PLACEHOLDER_LIST:
                self.text_field.text = ''
        elif self.text_field.text == '':
            self.text_field.text = self.placeholder_text


class IconCard(MDCard):
    def __init__(self, image_path: str, text: str, color=palette.blued_gray_main_rgba, func=None, data=None, **kwargs):
        super(IconCard, self).__init__(**kwargs)
        self.md_bg_color = color
        self.radius = appconf.CARD_RADIUS
        self.ripple_behavior = True
        self.on_release_func = func
        self.data = data

        grid = MDGridLayout(cols=2, padding=[60, 30, 30, 30])
        self.image = Image(source=image_path, allow_stretch=True, size_hint_x=.3)
        self.card_text = bfont.MSFont(text=text, style='Bold', size='20sp')

        grid.add_widget(self.card_text)
        grid.add_widget(self.image)

        self.add_widget(grid)

    def on_release(self):
        if self.on_release_func and self.data:
            self.on_release_func(self.data)
        else: self.on_release_func()

class ImageButton(ButtonBehavior, Image):
    def __init__(self, img_path, data=None, func=None, **kwargs):
        super().__init__(**kwargs)
        self.source = img_path
        self.data = data
        self.on_release_func = func

    def on_release(self):
        if self.on_release_func and self.data:
            self.on_release_func(self.data)
        else:
            self.on_release_func()

class Title(MDGridLayout):
    def __init__(self, screen_manager, goto='MainMenu', **kwargs):
        super(Title, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 50
        self.goto = goto
        back_button = ImageButton(img_path="images/back_button.png",
                                  func=lambda *a: self.backToMainMenu(screen_manager), size_hint_x=.15)
        self.add_widget(back_button)

    def backToMainMenu(self, screen_manager):
        change_screen(screen_manager, self.goto, 'right')


class AccentCard(MDCard):
    def __init__(self, text='', data=None, func=None, color=palette.accent_yellow_rgba, radius=20, text_size='12sp', **kwargs):
        super(AccentCard, self).__init__(**kwargs)
        grid = MDGridLayout(cols=1)
        self.radius = radius
        self.md_bg_color = color
        self.orf = func
        self.data = data
        self.ac_label = bfont.MSFont(text=text, style='Bold',
                                     halign='center', size=text_size)
        grid.add_widget(self.ac_label)
        self.add_widget(grid)

    def on_release(self):
        if self.orf:
            self.orf(self.data)

def convert_time(days: int):
    td = timedelta(days=days)
    ct = datetime.now()
    return datetime.strftime(td + ct, "%d.%m.%Y %H:%M MSK")


def dynamic_size(txl):
    return 25 if txl < 9 else 20 if txl < 12 else 17 if txl < 14 else 13
    # 20 if textlen > 9 else 15 if textlen > 12 else 25
