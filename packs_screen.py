from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
import bfont
import appconf
import certifi
import json
import elements
import dt
import cache_manager
import palette


class PacksScreen(MDScreen):
    def __init__(self, screen_manager):
        super(PacksScreen, self).__init__()
        self.name = "Packs"
        self.scr = screen_manager
        self.grid = MDGridLayout(cols=1, spacing=30, padding=appconf.OVERALL_PADDING)
        self.title = bfont.MSFont(text='Тарифы и планы', style='bold', size='25sp', size_hint_y=.5)
        self.CalcButton = elements.IconCard(image_path='images/profit_calculator.png',
                                            text='Расчитать доход',
                                            func=lambda *a: elements.change_screen(self.scr, "ProfitCalc"),
                                            color=palette.accent_yellow_rgba, size_hint_y=.5)

        self.title_lo = elements.Title(screen_manager, "MainMenu")
        self.title_lo.add_widget(self.title)


        self.grid.add_widget(self.title_lo)
        self.add_widget(self.grid)

        Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                  req_body=json.dumps({'method': 'DEPS_lookup'}),
                                                  on_success=self.success_ps,
                                                  on_error=self.error_ps,
                                                  timeout=appconf.REQUEST_TIMEOUT,
                                                  ca_file=certifi.where()), 0)

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.start_animate_all, 0)

    def on_leave(self, *args):
        Clock.schedule_once(self.stop_animate_all, 0)

    def pack_choose_handler(self, *args):
        Clock.schedule_once(lambda *a: cache_manager.Cache.get('Genesis', 'func_depscreen')(period=args[-1]), 0)
        elements.change_screen(self.scr, "DepositScreen")

    def create_dep_card(self, rdata: dict, *args):
        # print('CardCreation')
        for i in rdata.keys():
            self.grid.add_widget(item := self.PackItem(onreleasefunc=self.pack_choose_handler, data=i))
            item.pack_title.text = f"Вклад {rdata[i]['pack_meaning']}"
            bfaf_sum = 1000 + (1000 * rdata[i]['percent']) / 100
            item.after_card.ac_label.text = f"{dt.MoneyData(bfaf_sum).AM_TEXT}"
            item.profitcard_title.ac_label.text = f"{rdata[i]['percent']}%"
            item.pack_description.text = f"Дней до выплаты: {i}"
        self.grid.add_widget(self.CalcButton)


    def success_ps(self, *args):
        r = json.loads(args[-1])
        Clock.schedule_once(lambda *a: self.create_dep_card(r), 0)

    def error_ps(self, *args):
        ...

    def start_animate_all(self, *args):
        ...

    def stop_animate_all(self, *args):
        ...

    class PackItem(MDCard):
        def __init__(self, onreleasefunc=None, data=None, **kwargs):
            super().__init__(**kwargs)
            self.orf = onreleasefunc
            self.data = data
            self.radius = appconf.CARD_RADIUS
            self.md_bg_color = palette.blued_gray_main_rgba

            main_grid = MDGridLayout(cols=2, padding=[30])
            elem_grid = MDGridLayout(cols=1, rows=3, spacing=10)

            title_grid = MDGridLayout(cols=2)
            self.pack_title = bfont.MSFont(text='', style='Bold', size='20sp', size_hint_x=.7)
            self.profitcard_title = elements.AccentCard(size_hint_x=.3, func=onreleasefunc, data=data)
            title_grid.add_widget(self.pack_title)
            title_grid.add_widget(self.profitcard_title)

            bfaf_grid = MDGridLayout(cols=4, rows=1, spacing=20)
            self.before_card = elements.AccentCard('1000 ₽', size_hint_x=.3, color=palette.white_rgba,
                                                   func=onreleasefunc, data=data)
            separator = bfont.MSFont(text='>>', style='Bold', size='15sp',
                                     halign='center', size_hint_x=.1)
            self.after_card = elements.AccentCard('... ₽', size_hint_x=.4, func=onreleasefunc, data=data)
            bfaf_grid.add_widget(self.before_card)
            bfaf_grid.add_widget(separator)
            bfaf_grid.add_widget(self.after_card)
            bfaf_grid.add_widget(MDBoxLayout(size_hint_x=.4))

            self.pack_description = bfont.MSFont(text='', size='15sp')
            self.arrow = elements.Image(source='images/arrow.png', size_hint_x=.1, allow_stretch=True)

            elem_grid.add_widget(title_grid)
            elem_grid.add_widget(bfaf_grid)
            elem_grid.add_widget(self.pack_description)

            main_grid.add_widget(elem_grid)
            main_grid.add_widget(self.arrow)
            self.add_widget(main_grid)

        def on_release(self):
            if self.orf:
                self.orf(self.data)
