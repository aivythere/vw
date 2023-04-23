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

        main_grid = MDGridLayout(cols=1, spacing=50, padding=[100, 100, 100, 100])
        self.pic = Image(source='images/congratz.png', allow_stretch=True)
        congratz_text = bfont.MSFont("Поздравляем!\nВклад открыт", style='Bold', halign='center')
        self.period_summ_text = bfont.MSFont(f"Период: [font=fonts/MS_Bold]0[/font]\n"
                                             f"Сумма: [font=fonts/MS_Bold]0[/font]", size="25sp", halign='center')
        self.payout_info_text = bfont.MSFont(f"Выплата: [font=fonts/MS_Bold]0[/font]\n"
                                             f"Прибыль: [font=fonts/MS_Bold]0[/font]", size="25sp", halign='center')
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
            on_release=self.escapeScreen
        )

        main_grid.add_widget(self.pic)
        main_grid.add_widget(congratz_text)
        main_grid.add_widget(self.period_summ_text)
        main_grid.add_widget(self.payout_info_text)
        main_grid.add_widget(self.menu_button)

        self.add_widget(main_grid)


    def escapeScreen(self, *args):
        elements.change_screen(self.scr, "MainMenu", no_ts=True)
        Clock.schedule_once(lambda *a: self.scr.remove_widget(self), 1)

    def update(self, period, summ, payout, profit):

        self.period_summ_text.text =\
            f"Период: [font=fonts/MS_Bold]{period} {'день' if int(period) == 1 else 'дней'}[/font]\n" \
            f"Сумма: [font=fonts/MS_Bold]{dt.MoneyData(summ).AM_TEXT}[/font]"

        self.payout_info_text.text = f"Выплата: [font=fonts/MS_Bold]{dt.MoneyData(payout).AM_TEXT}[/font]\n" \
                                     f"Прибыль: [font=fonts/MS_Bold]{dt.MoneyData(profit).AM_TEXT}[/font]"
