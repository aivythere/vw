from datetime import timedelta, datetime

from kivy.graphics import *
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
import bfont
import palette
import appconf
import animations
import dt
from kivy.core.window import Window


def change_screen(screen_manager, to_sc, ts_dir='left', no_ts=False):
    if not no_ts:
        screen_manager.transition = appconf.DEFAULT_TRANSITION
        screen_manager.transition.direction = ts_dir
        screen_manager.current = to_sc
        return
    screen_manager.transition = NoTransition()
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
    def __init__(self, on_text_change, placeholder='', **kwargs):
        super(BetterMoneyTextInput, self).__init__(**kwargs)
        self.md_bg_color = palette.blued_gray_main_rgba
        self.padding = 20
        self.radius = 40
        self.placeholder_text = placeholder

        grid = MDGridLayout(cols=2)
        self.input_text_card = MDCard(
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
            input_filter='int',
            input_type='number',
            text=placeholder
        )
        opg.add_widget(self.text_field)
        self.clear_btn = ImageButton('images/clear.png', func=self.clear_text, pos_hint={'center_x': .9, 'center_y': .35},
                        size_hint_x=.1, allow_stretch=True)
        opg.add_widget(
            self.clear_btn
        )
        self.input_text_card.add_widget(opg)
        self.text_field.bind(
            text=on_text_change,
            focus=self.is_placeholder
        )

        grid.add_widget(self.input_text_card)
        grid.add_widget(
            bfont.MSFont(
                text="₽", style='Bold', size='40sp', halign='center', valign='center',
                size_hint_x=.1, text_color=(0, 0, 0, 1), theme_text_color="Custom"
            )
        )
        self.add_widget(grid)

    def is_placeholder(self, *args):
        if args[-1]:
            if self.text_field.text in appconf.PLACEHOLDER_LIST:
                self.text_field.text = ''
        elif self.text_field.text == '':
            self.text_field.text = self.placeholder_text

    def clear_text(self, *args):
        if self.text_field.text not in appconf.PLACEHOLDER_LIST:
            animations.backbutton_opacity(dur=.1).start(self.clear_btn)
            self.text_field.text = ''


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
        self.input_text_card = MDCard(
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

        self.input_text_card.add_widget(opg)
        self.text_field.bind(
            text=on_text_change,
            focus=self.is_placeholder
        )

        grid.add_widget(self.input_text_card)
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
        else:
            self.on_release_func()


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
        self.back_button = ImageButton(img_path="images/back_button.png",
                                       func=lambda *a: self.backToMainMenu(screen_manager), size_hint_x=.15)
        self.add_widget(self.back_button)

    def backToMainMenu(self, screen_manager):
        animations.backbutton_opacity().start(self.back_button)
        change_screen(screen_manager, self.goto, 'right')


class AccentCard(MDCard):
    def __init__(self, text='', data=None, func=None, color=palette.accent_yellow_rgba, radius=20, text_size='12sp',
                 **kwargs):
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


class ApproveBuyPopup(MDDialog):
    def __init__(self, sum, per, pyo, prf, date, baf, **kwargs):
        self.type = "custom"
        self.content_cls = self.Contents(sum, per, pyo, prf, date, baf, self.dismiss)

        self.size_hint = [None, None]
        self.width = Window.width - 50
        self.height = self.content_cls.height

        self.opacity = 0
        self.dismissable = True
        self.elevation = 0
        super(ApproveBuyPopup, self).__init__(**kwargs)

    def on_pre_open(self):
        super(ApproveBuyPopup, self).on_pre_open()
        animations.backbutton_opacity(0, 1, .1).start(self)

    def dismiss(self, *_args, **kwargs):
        if self.dismissable or kwargs.get('force_close'):
            super(ApproveBuyPopup, self).dismiss()

    class Contents(MDGridLayout):
        def __init__(self, sum_raw, period_raw, payout_raw, profit_raw,
                     date_cooked, buy_approve_func, dismiss_func, **kwargs):
            super().__init__(**kwargs)
            self.size_hint_y = None
            self.height = sp(300)

            self.rows = 3
            self.md_bg_color = (0, 0, 0, 0)
            self.padding = [0, 0, 0, 30]

            checkmark_icon = Image(source='images/check.png', allow_stretch=True, size_hint_y=.3)
            label = bfont.MSFont(text=f'Сумма: [font=fonts/MS_Bold]{sum_raw}[/font]\n'
            # дней
                                      f'Период: [font=fonts/MS_Bold]{period_raw} {"день" if int(period_raw) == 1 else "дней"}[/font]\n'
                                      f'Сумма выплаты: [font=fonts/MS_Bold]{payout_raw}[/font]\n'
                                      f'Прибыль: [font=fonts/MS_Bold]{profit_raw}[/font]\n'
                                      f'Дата выплаты:\n [font=fonts/MS_Bold]~{date_cooked}[/font]', halign='center',
                                 size="20sp")
            #  < \n
            btn_layout = MDGridLayout(cols=2, rows=1, spacing=30, size_hint_y=.3)
            self.approve_button = MDCard(
                bfont.MSFont(
                    text='Подтвердить', halign='center',
                    style="Bold", size="15sp", color=palette.black_rgba
                ),
                md_bg_color=palette.accent_yellow_rgba,
                on_release=buy_approve_func,
                ripple_behavior=True,
                radius=40
            )
            self.decline_button = MDCard(
                bfont.MSFont(
                    text='Отменить', halign='center',
                    style="Bold", size="15sp"
                ),
                md_bg_color=palette.blued_gray_main_rgba,
                on_release=dismiss_func,
                ripple_behavior=True,
                radius=40
            )

            btn_layout.add_widget(self.decline_button)
            btn_layout.add_widget(self.approve_button)

            self.add_widget(checkmark_icon)
            self.add_widget(label)
            self.add_widget(btn_layout)


class PackInfoPopup(MDDialog):
    # pass
    def __init__(self, od, os, cd, cs, **kwargs):
        self.type = "custom"
        self.content_cls = self.Contents(od, os, cd, cs, self.dismiss)

        self.size_hint = [None, None]
        self.width = Window.width - 50
        self.height = self.content_cls.height

        self.opacity = 0
        self.dismissable = True
        self.elevation = 0
        super(PackInfoPopup, self).__init__(**kwargs)

    def on_pre_open(self):
        super(PackInfoPopup, self).on_pre_open()
        animations.backbutton_opacity(0, 1, .1).start(self)

    def dismiss(self, *_args, **kwargs):
        if self.dismissable or kwargs.get('force_close'):
            super(PackInfoPopup, self).dismiss(force=True)

    class Contents(MDGridLayout):
        def __init__(self, open_date, open_sum_raw, close_date, close_sum_raw, dismiss_func, **kwargs):
            super().__init__(**kwargs)
            self.size_hint_y = None
            self.height = sp(400)
            self.size_hint_x = 1.5
            self.rows = 3
            self.md_bg_color = (0, 0, 0, 0)
            self.spacing = 30
            self.padding = [0, 0, 0, 30]

            profit = close_sum_raw - open_sum_raw
            daysleft = ((strtodt(close_date) - strtodt(open_date)).days)

            self.add_widget(
                bfont.MSFont(
                    "Информация", halign='center', style='Bold',
                    size_hint_y=.1, size="25sp"
                )
            )

            self.add_widget(
                bfont.MSFont(
                    f"Дата открытия: [font=fonts/MS_Bold]{open_date}[/font]\n"
                    f"Сумма открытия: [font=fonts/MS_Bold]{dt.MoneyData(open_sum_raw).AM_TEXT}[/font]\n\n"
                    f""
                    f"Дата закрытия: [font=fonts/MS_Bold]{close_date}[/font]\n"
                    f"Сумма закрытия: [font=fonts/MS_Bold]{dt.MoneyData(close_sum_raw).AM_TEXT}[/font]\n\n"
                    f""
                    f"Прибыль: [font=fonts/MS_Bold]{dt.MoneyData(profit).AM_TEXT}[/font]\n"
                    f"До выплаты (дней): [font=fonts/MS_Bold]{daysleft}[/font]",
                    size="20sp", size_hint_y=1.2
                )
            )

            self.add_widget(
                MDCard(
                    bfont.MSFont(
                        "Закрыть", style="Bold", halign="center", size="25sp"
                    ),
                    md_bg_color=palette.blued_gray_main_rgba,
                    radius=appconf.CARD_RADIUS,
                    on_release=dismiss_func,
                    ripple_behavior=True,
                    size_hint_y=.5
                )
            )


class ErrorPopup(MDDialog):
    def __init__(self, **kwargs):
        self.type = "custom"
        self.content_cls = self.ERRPopupFilling()

        self.size_hint = [None, None]
        self.width = Window.width - 50
        self.height = self.content_cls.height

        self.opacity = 0
        self.elevation = 0
        self.radius = [appconf.CARD_RADIUS for _ in range(4)]
        super(ErrorPopup, self).__init__(**kwargs)

    def dismiss(self, *_args, **kwargs):
        super(ErrorPopup, self).dismiss(force=True)

    def on_pre_open(self):
        super(ErrorPopup, self).on_pre_open()
        animations.backbutton_opacity(0, 1, .1).start(self)

    class ERRPopupFilling(ButtonBehavior, MDGridLayout):
        def __init__(self, df=None):
            super().__init__()
            self.size_hint_y = None
            self.height = sp(300)
            self.rows = 3
            self.padding = [0, 0, 0, 30]
            self.md_bg_color = (0, 0, 0, 0)
            self.spacing = 30

            self.pic = Image(source='images/error.png', allow_stretch=True, size_hint_y=.5,
                             pos_hint={'center_x': .5, 'center_y': .5})
            self.errlabel = bfont.MSFont("[font=fonts/MS_Bold]Ошибка сети[/font]\n\n"
                                         "[size=20sp]Не можем подключиться к серверу, проверьте свой интернет "
                                         f"или узнайте состояние серверов на {appconf.DOMAIN}[/size]",
                                         halign='center')
            self.add_widget(self.pic)
            self.add_widget(self.errlabel)

        def on_release(self):
            print('w')


def convert_time(days: int):
    td = timedelta(days=int(days))
    ct = datetime.now()
    return datetime.strftime(td + ct, "%d.%m.%Y %H:%M MSK")


def dynamic_size(txl):
    return 25 if txl < 12 else 20 if txl < 14 else 17 if txl < 18 else 15
    # 20 if textlen > 9 else 15 if textlen > 12 else 25


def cash(summ, perc, prof=False, wrap_in_dt=False):
    if not prof:
        res = round(((float(summ) * float(perc)) / 100) + float(summ), 2)
        if not wrap_in_dt:
            return res
        else:
            return dt.MoneyData(res).AM_TEXT
    if not wrap_in_dt:
        return round(((float(summ) * float(perc)) / 100) + float(summ) - summ, 2)
    else:
        return dt.MoneyData(round(((float(summ) * float(perc)) / 100) + float(summ) - summ, 2)).AM_TEXT


def dayordays(per):
    if int(per) == 1:
        return "день"
    return "дней"


def strtodt(_str: str):
    _str = _str.replace(" MSK", "")
    dt_object = datetime.strptime(_str, '%d.%m.%Y %H:%M')
    return dt_object

def around(obj_pos, touch_x, touch_y):
    if touch_x: ...