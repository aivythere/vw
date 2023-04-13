import json
import sqlite3
import certifi
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import sp
from kivy.network.urlrequest import UrlRequest
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard, MDSeparator
import animations
import bfont
import palette
import elements
import appconf
import dt


class ProfitCalculatorScreen(MDScreen):
    def __init__(self, screen_manager):
        super(ProfitCalculatorScreen, self).__init__()
        self.name = 'ProfitCalc'
        grid = MDGridLayout(cols=1, padding=appconf.OVERALL_PADDING, spacing=50)
        self.title = bfont.MSFont(text='Загрузка...', style='Bold', size='25sp', size_hint_y=.3)
        self.title_lo = elements.Title(screen_manager)
        self.title_lo.add_widget(self.title)

        self.deposit_amount_card = elements.TextCard(main_text='', sec_text='Сумма вклада')
        self.min_dep_amount_label = bfont.MSFont('от 100 ₽ до 50 000 000 ₽', size='15sp',
                                                 size_hint_y=0.1, halign='center', valign='center')
        self.deposit_amount_input = elements.BetterMoneyTextInput(
            on_text_change=self.onTextFieldTextChange,
        )
        self.deposit_amount_input.disabled = True
        # separator
        grid.add_widget(self.title_lo)
        grid.add_widget(self.deposit_amount_card)
        grid.add_widget(self.min_dep_amount_label)
        grid.add_widget(self.deposit_amount_input)
        self.PeriodButtons_instance = self.PeriodButtons(self.choose_period)
        grid.add_widget(self.PeriodButtons_instance)
        grid.add_widget(MDSeparator(size_hint_y=.2))
        self.ProfitCard_instance = self.ProfitCard()
        grid.add_widget(self.ProfitCard_instance)

        self.add_widget(grid)

        self.MYID = None
        self.CALC_DATA = None
        self.CHOSEN_PERIOD = '1'
        self.DEPOSIT_SUM = 100
        self.PERIOD_BUTTONS_LIST = [self.PeriodButtons_instance.b1, self.PeriodButtons_instance.b2,
                                    self.PeriodButtons_instance.b3, self.PeriodButtons_instance.b4]
        self.REQUEST_ERR_COUNT = 0

    def success_calcdata(self, *args):
        # 3
        response = json.loads(args[-1])
        self.CALC_DATA = response
        Clock.schedule_once(self.stop_animate_all, 0)
        self.title.text = 'Рассчитать доход'
        self.PeriodButtons_instance.disabled = False
        self.deposit_amount_input.disabled = False
        self.deposit_amount_card.main_text.text = dt.MoneyData(self.DEPOSIT_SUM).AM_TEXT
        self.ProfitCard_instance.profit_label.text = f"[size=30sp]{dt.MoneyData(self.DEPOSIT_SUM/100*self.CALC_DATA[self.CHOSEN_PERIOD]['percent']).AM_TEXT}[/size]" \
                                                     f"[size=15sp]\nприбыль[/size]"
        self.ProfitCard_instance.profit_summary_label.text = f"{dt.MoneyData(self.DEPOSIT_SUM+self.DEPOSIT_SUM/100*self.CALC_DATA[self.CHOSEN_PERIOD]['percent']).AM_TEXT} итого"
        self.ProfitCard_instance.payout_date_label.text = f"Дата выплаты\n" \
                                                          f"~[font=fonts/MS_Bold]{elements.convert_time(int(self.CHOSEN_PERIOD))}[/font]"
        self.ProfitCard_instance.period_label.text = self.CALC_DATA[self.CHOSEN_PERIOD]['name']


    def error_calcdata(self, *args):
        self.REQUEST_ERR_COUNT += 1
        if self.REQUEST_ERR_COUNT >= appconf.REQUEST_ERR_COUNTOUT:
            NETWORK_ERR_POPUP = MDDialog(type="custom", content_cls=elements.ERRPopupFilling())
            NETWORK_ERR_POPUP.open()
        else:
            Clock.schedule_once(
                lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN, req_body=json.dumps({"method": "CALCREQUEST"}),
                                      on_success=self.success_calcdata, on_error=self.error_calcdata,
                                      timeout=appconf.REQUEST_TIMEOUT,
                                      ca_file=certifi.where()), appconf.REQUEST_RETRY_INTERVAL)

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.start_animate_all, 0)
        Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN, req_body=json.dumps({"method": "CALCREQUEST"}),
                                                  on_success=self.success_calcdata, on_error=self.error_calcdata,
                                                  timeout=appconf.REQUEST_TIMEOUT,
                                                  ca_file=certifi.where()), 0)

        # animations.change_size_anim().start(self.PERIOD_BUTTONS_LIST[0])
        self.PERIOD_BUTTONS_LIST[0].md_bg_color = palette.accent_yellow_rgba

    def on_leave(self, *args):
        Clock.schedule_once(self.stop_animate_all, 0)
        Clock.schedule_once(lambda *a: self.choose_period(self.PERIOD_BUTTONS_LIST[0], 1))

    def choose_period(self, *args):
        self.CHOSEN_PERIOD = str(args[1])
        instance = args[0]

        animations.change_size_anim().start(instance)
        instance.md_bg_color = palette.accent_yellow_rgba

        for i in self.PERIOD_BUTTONS_LIST:
            if i != instance:
                animations.change_size_anim(False).start(i)
                i.md_bg_color = palette.blued_gray_main_rgba

        Clock.schedule_once(self.refresh_elements, 0)

    def moveCursor(self, *args):
        self.deposit_amount_input.text_field.cursor = (len(self.deposit_amount_input.text_field.text) + 1, 0)

    def onTextFieldTextChange(self, *args):
        value = args[-1].replace(" ", "")
        if value == '':
            self.DEPOSIT_SUM = 100
            Clock.schedule_once(self.refresh_elements, 0)

        if value.isdigit():
            self.deposit_amount_card.main_text.text = dt.MoneyData(value).AM_TEXT
            self.DEPOSIT_SUM = int(value)
            Clock.schedule_once(self.refresh_elements, 0)
            if len(value) >= 4:
                self.deposit_amount_input.text_field.text = dt.decorateNumberDigits(value, nofloat=True)
                Clock.schedule_once(self.moveCursor, 0)
            if int(value) < 100:
                animations.change_text_color_anim(palette.unavailable_red).start(self.deposit_amount_card.main_text)
            else:
                animations.change_text_color_anim(appconf.PRIMARY_TEXT_COLOR).start(self.deposit_amount_card.main_text)

    def refresh_elements(self, *args):
        textlen = len(dt.MoneyData(self.DEPOSIT_SUM / 100 * self.CALC_DATA[self.CHOSEN_PERIOD]['percent']).AM_TEXT)
        self.ProfitCard_instance.profit_label.font_size = sp(25-textlen/10)
        self.deposit_amount_card.main_text.text = dt.MoneyData(self.DEPOSIT_SUM).AM_TEXT
        self.ProfitCard_instance.profit_label.text = f"[size={elements.dynamic_size(textlen)}sp]{dt.MoneyData(self.DEPOSIT_SUM / 100 * self.CALC_DATA[self.CHOSEN_PERIOD]['percent']).AM_TEXT}[/size]" \
                                                     f"[size=15sp]\nприбыль[/size]"
        self.ProfitCard_instance.profit_summary_label.text = f"{dt.MoneyData(self.DEPOSIT_SUM + self.DEPOSIT_SUM / 100 * self.CALC_DATA[self.CHOSEN_PERIOD]['percent']).AM_TEXT} итого"
        self.ProfitCard_instance.payout_date_label.text = f"Дата выплаты\n" \
                                                          f"~[font=fonts/MS_Bold]{elements.convert_time(int(self.CHOSEN_PERIOD))}[/font]"
        self.ProfitCard_instance.period_label.text = f"[size=25sp]{self.CALC_DATA[self.CHOSEN_PERIOD]['name']}[/size]" \
                                                     f"[size=15dp]\n{self.CALC_DATA[self.CHOSEN_PERIOD]['percent']}%[/size]"

    def start_animate_all(self, *args):
        animations.load_animation().start(self.deposit_amount_card)
        animations.load_animation().start(self.PeriodButtons_instance)
        animations.load_animation().start(self.ProfitCard_instance)

    def stop_animate_all(self, *args):
        Animation.stop_all(self.deposit_amount_card)
        Animation.stop_all(self.PeriodButtons_instance)
        Animation.stop_all(self.ProfitCard_instance)

        self.deposit_amount_card.opacity = 1
        self.PeriodButtons_instance.opacity = 1
        self.ProfitCard_instance.opacity = 1

    class ProfitCard(MDCard):
        def __init__(self):
            super().__init__()
            self.padding = 30
            self.md_bg_color = palette.blued_gray_main_rgba
            master_grid = MDGridLayout(rows=3, cols=1)
            self.size_hint_y = 2.5
            self.radius = 40

            profit_text_grid = MDGridLayout(cols=2, rows=1)
            self.profit_label = bfont.MSFont(text='[size=20sp]...[/size]'
                                                  '[size=15sp]\nприбыль[/size]',
                                             color=palette.dark_green,
                                             style='Bold')
            self.period_label = bfont.MSFont(text='1 месяц', size='25sp', style='Bold', halign='right')

            self.profit_summary_label = bfont.MSFont(text='...', size='20sp', style='Bold')

            payout_date_approx_grid = MDGridLayout(cols=2, rows=1, spacing=30)
            payout_date_approx_grid.add_widget(
                Image(source='images/calendar.png', allow_stretch=True, size_hint_y=.2, size_hint_x=.2
                      ))
            self.payout_date_label = bfont.MSFont(text='Дата выплаты\n'
                                                       '[font=fonts/MS_Bold]~...[/font]',
                                                  style='Medium', size='15sp', halign='left',
                                                  )

            profit_text_grid.add_widget(self.profit_label)
            profit_text_grid.add_widget(self.period_label)

            payout_date_approx_grid.add_widget(self.payout_date_label)

            master_grid.add_widget(profit_text_grid)
            master_grid.add_widget(self.profit_summary_label)
            master_grid.add_widget(payout_date_approx_grid)

            self.add_widget(master_grid)

    class PeriodButtons(MDGridLayout):
        def __init__(self, choose_period_func):
            super().__init__()
            self.cols = 4
            self.rows = 1
            self.spacing = 20
            self.size_hint_y = .5
            self.disabled = True

            self.b1 = self.PeriodButton(choose_period_func, '1 день', 1)
            self.b2 = self.PeriodButton(choose_period_func, '7 дней', 7)
            self.b3 = self.PeriodButton(choose_period_func, '30 дней', 30)
            self.b4 = self.PeriodButton(choose_period_func, '90 дней', 90)

            self.add_widget(self.b1)
            self.add_widget(self.b2)
            self.add_widget(self.b3)
            self.add_widget(self.b4)

        class PeriodButton(MDCard):
            def __init__(self, on_release_func, text, period: int):
                super().__init__()
                self.md_bg_color = palette.blued_gray_main_rgba
                self.radius = 20
                self.on_release_func = on_release_func
                self.period = period
                self.size_hint_y = .3
                g = MDGridLayout(
                    bfont.MSFont(
                        text=text, halign='center', size='13sp',
                        valign='center', style='Bold'
                    ),
                    cols=1,
                    rows=1
                )
                self.add_widget(g)

            def on_release(self):
                Clock.schedule_once(lambda *a: self.on_release_func(self, self.period), 0)

#
# class LakeApp(MDApp):
#     def build(self):
#         self.title = "PFSCREEN"
#         sm = MDScreenManager()
#         sw = ProfitCalculatorScreen()
#         sm.add_widget(sw)
#         # TEST
#         Window.size = (350, 650)
#         sm.current = "ProfitCalc"
#         return sm
#
#
# LakeApp().run()
