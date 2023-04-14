import json
import sqlite3
import certifi
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.slider import MDSlider
import animations
import bfont
import palette
import elements
import appconf
import dt

class DepositScreen(MDScreen):

    def __init__(self, screen_manager):
        super().__init__()
        self.name = "DepositScreen"
        main_grid = MDGridLayout(cols=1, padding=appconf.OVERALL_PADDING, spacing=40)

        self.title = bfont.MSFont(text='Загрузка...', style='Bold', size='25sp', size_hint_y=.3)
        self.title_lo = elements.Title(screen_manager, 'Packs')
        self.title_lo.add_widget(self.title)

        self.BALANCE_card = elements.TextCard(main_text='', sec_text='Доступные средства')
        # separator
        self.deposit_amount_card = elements.TextCard(main_text=dt.MoneyData(100).AM_TEXT)
        self.slider = MDSlider(
                thumb_color_active = palette.accent_yellow_rgba,
                color = palette.blued_gray_main_rgba,
                thumb_color_inactive = palette.accent_yellow_rgba,
                hint = False,
                min = 100,
                max = 100,
                step = 50,
                show_off = False,
                size_hint_y = .3,
                disabled = True
            )
        self.slider.bind(value=self.onSlider)
        self.sum_textfield = elements.BetterMoneyTextInput(on_text_change=self.onTextFieldTextChange)
        self.sum_textfield.disabled = True
        self.ProfitCard_instance = self.ProfitCard()
        self.OpenDepositButton_instance = self.OpenDepositButton(lambda *a: print('opendep func line 50'))

        main_grid.add_widget(self.title_lo)
        main_grid.add_widget(self.BALANCE_card)
        main_grid.add_widget(MDSeparator())
        main_grid.add_widget(self.deposit_amount_card)
        main_grid.add_widget(bfont.MSFont(text=f'Минимальная сумма вклада - {dt.MoneyData(100).AM_TEXT}',
                                          size="15sp", halign='center', size_hint_y=.1))
        main_grid.add_widget(self.slider)
        main_grid.add_widget(self.sum_textfield)
        main_grid.add_widget(bfont.MSFont(text='Ваш заработок',
                                          size="15sp", halign='center', size_hint_y=.1))
        main_grid.add_widget(self.ProfitCard_instance)
        main_grid.add_widget(self.OpenDepositButton_instance)

        self.add_widget(main_grid)

        self.DEP_PERIOD = None
        self.MYID = None
        self.BALANCE = 0
        self.PERCENT = 0
        self.REQUEST_ERR_COUNT = 0
        self.REQUEST_INSTANCE = None
        self.IS_ANIM_ONGO = False

    def grab_my_id(self, *args):
        cursor = sqlite3.connect(appconf.LOCAL_DB_FILENAME).cursor()
        MY_ID = cursor.execute("SELECT my_id FROM data").fetchone()
        if MY_ID is not None:
            self.MYID = MY_ID[0]

    def success_lookup(self, *args):
        response = json.loads(args[-1])
        if response['period'] == self.DEP_PERIOD:
            Clock.schedule_once(self.stop_animate_all, 0)
            self.IS_ANIM_ONGO = False
            self.BALANCE = response['balance']
            self.PERCENT = response['percent']
            self.title.text = f"Вклад {response['pack_meaning']}"
            if self.BALANCE > 2000:
                self.slider.step = 100
            self.OpenDepositButton_instance.disabled = False
            self.slider.max = self.BALANCE
            self.slider.disabled = False
            self.sum_textfield.disabled = False
            self.BALANCE_card.main_text.text = dt.MoneyData(self.BALANCE).AM_TEXT
            self.ProfitCard_instance.profit_amount.text = f"[size=20sp]{dt.MoneyData((100 / 100) * self.PERCENT).AM_TEXT}[/size]"\
                                                   f"[size=13sp]\n{dt.MoneyData(100 + (100 / 100) * self.PERCENT).AM_TEXT}[/size]"
            self.ProfitCard_instance.profit_percent.text = f"{self.PERCENT}%"

    def error_lookup(self, *args):
        self.REQUEST_ERR_COUNT += 1
        if self.REQUEST_ERR_COUNT >= appconf.REQUEST_ERR_COUNTOUT:
            NETWORK_ERR_POPUP = MDDialog(type="custom", content_cls=elements.ERRPopupFilling())
            NETWORK_ERR_POPUP.open()
        else:
            Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                    req_body=json.dumps({'method': 'OV_lookup', 'my_id': self.MYID, 'dep_period': self.DEP_PERIOD}),
                    on_success=self.success_lookup, on_error=self.error_lookup,
                    timeout=appconf.REQUEST_TIMEOUT,
                    ca_file=certifi.where()), appconf.REQUEST_RETRY_INTERVAL)

    def reload(self, period):
        self.DEP_PERIOD = period

    def on_pre_enter(self, *args):
        if not self.IS_ANIM_ONGO:
            Clock.schedule_once(self.start_animate_all, 0)
            self.IS_ANIM_ONGO = True
        Clock.schedule_once(self.grab_my_id)
        self.REQUEST_INSTANCE = Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                    req_body=json.dumps({'method': 'OV_lookup', 'my_id': self.MYID, 'dep_period': self.DEP_PERIOD}),
                    on_success=self.success_lookup, on_error=self.error_lookup,
                    timeout=appconf.REQUEST_TIMEOUT,
                    ca_file=certifi.where()), 0)


    def on_leave(self, *args):
        self.REQUEST_INSTANCE.cancel()
        self.title.text = "Загрузка"
        self.BALANCE_card.main_text.text = ""
        self.slider.value = 100
        self.slider.disabled = True
        self.OpenDepositButton_instance.disabled = True
        self.deposit_amount_card.main_text.text = dt.MoneyData(100).AM_TEXT
        self.ProfitCard_instance.profit_amount.text = "..."
        self.ProfitCard_instance.profit_percent.text = "...%"
        self.sum_textfield.text_field.text = ""

    def start_animate_all(self, *args):
        animations.load_animation().start(self.deposit_amount_card)
        animations.load_animation().start(self.ProfitCard_instance)
        animations.load_animation().start(self.BALANCE_card)
        animations.load_animation().start(self.slider)

    def stop_animate_all(self, *args):
        Animation.stop_all(self.deposit_amount_card)
        Animation.stop_all(self.ProfitCard_instance)
        Animation.stop_all(self.BALANCE_card)
        Animation.stop_all(self.slider)

        self.deposit_amount_card.opacity = 1
        self.ProfitCard_instance.opacity = 1
        self.BALANCE_card.opacity = 1
        self.slider.opacity = 1

    def moveCur(self, *args):
        self.sum_textfield.text_field.cursor = (len(self.sum_textfield.text_field.text) + 1, 0)

    def onTextFieldTextChange(self, *args):
        value = args[-1].replace(" ", "")
        if value == '':
            self.slider.value = self.slider.min
        if value.isdigit():
            # if len(value) >= 4:
            #     self.sum_textfield.text_field.text = dt.decorateNumberDigits(value, nofloat=True)
            #     Clock.schedule_once(self.moveCur, 0)
            if float(value) <= self.BALANCE:
                self.deposit_amount_card.main_text.text = dt.MoneyData(value).AM_TEXT
                animations.slider_anim(value).start(self.slider)
                animations.change_text_color_anim(appconf.PRIMARY_TEXT_COLOR).start(self.deposit_amount_card.main_text)
            else:
                animations.change_text_color_anim(palette.unavailable_red).start(self.deposit_amount_card.main_text)
                self.slider.value = self.slider.max

    def onSlider(self, *args):
        value = args[-1]
        self.deposit_amount_card.main_text.text = dt.MoneyData(value).AM_TEXT
        self.ProfitCard_instance.profit_amount.text = dt.MoneyData((value/100)*self.PERCENT).AM_TEXT
        self.ProfitCard_instance.profit_amount.text=f"[size=20sp]{dt.MoneyData((value/100)*self.PERCENT).AM_TEXT}[/size]" \
                                                  f"[size=13sp]\n{dt.MoneyData(value+(value/100)*self.PERCENT).AM_TEXT}[/size]"
        if float(value) <= self.BALANCE:
            self.deposit_amount_card.main_text.text_color = appconf.PRIMARY_TEXT_COLOR
        else:
            self.deposit_amount_card.main_text.text_color = palette.unavailable_red

        if float(value) < 100:
            self.slider.value = self.slider.min

    class ProfitCard(MDCard):
        def __init__(self):
            super().__init__()
            grid = MDGridLayout(cols=2, padding=30)
            self.md_bg_color = palette.blued_gray_main_rgba
            self.radius = appconf.CARD_RADIUS
            self.profit_amount = bfont.MSFont(text=f"...", halign='left',
                                              style="Bold", color=palette.dark_green)
            self.profit_percent = bfont.MSFont(text=f"...%", halign='right', style="Bold",
                                               color=palette.dark_green, size="25sp")
            grid.add_widget(self.profit_amount)
            grid.add_widget(self.profit_percent)
            self.add_widget(grid)

    class OpenDepositButton(MDCard):
        def __init__(self, open_deposit_func):
            super().__init__()
            self.open_dep_func = open_deposit_func
            self.md_bg_color = palette.accent_yellow_rgba
            self.padding = 40
            self.radius = appconf.CARD_RADIUS
            self.size_hint_y = .8
            self.ripple_behavior = True
            self.disabled = True
            self.add_widget(
                bfont.MSFont(text='Открыть вклад', style='Bold', size="20sp", halign='center')
            )

        def on_release(self):
            self.open_dep_func()
            self.size = [self.size[0] - 20, self.size[1] - 20]

#
# class LakeApp(MDApp):
#     def build(self):
#         self.title = "DEPSCREEN"
#         sm = MDScreenManager()
#         sw = DepositScreen()
#         sw.reload(7)
#         sm.add_widget(sw)
#         # TEST
#         Window.size = (350, 650)
#         sm.current = "DepositScreen"
#         return sm
#
# LakeApp().run()