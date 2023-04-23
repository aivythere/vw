import sqlite3
from kivy.animation import Animation
from kivy.network.urlrequest import UrlRequest
import dt
import animations
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard, MDSeparator
import bfont
import palette
import appconf
import certifi
import json
import elements


class MainMenuScreen(MDScreen):
    def __init__(self, screen_manager):
        super(MainMenuScreen, self).__init__()
        self.name = 'MainMenu'
        self.screen_manager = screen_manager
        # self.depscreen_instance = dep_sc_in
        grid = MDGridLayout(cols=1, spacing=40, padding=appconf.OVERALL_PADDING)

        self.title = bfont.MSFont(text='Главное меню', style='Bold', size='35sp', size_hint_y=.5)
        self.ProfileCard_instance = self.ProfileCard()
        # separator
        self.OpenDeposit_button = elements.IconCard(text='Открыть вклад', image_path='images/open_deposit.png',
                                                    size_hint_y=.5,
                                                    func=self.screenHandler, data="OpenDeposit", disabled=True)
        self.MyDeposits_button = elements.IconCard(text='Мои вклады', image_path='images/my_deposits.png',
                                                   size_hint_y=.5,
                                                   func=self.screenHandler, data="MyDeposits", disabled=True)
        self.ProfitCalc_button = elements.IconCard(text='Расчет дохода', image_path='images/profit_calculator.png',
                                                   size_hint_y=.5,
                                                   func=self.screenHandler, data="ProfitCalc", disabled=True)
        self.RefferalProgram_button = elements.IconCard(text='Рефералы', image_path='images/referral.png',
                                                        size_hint_y=.5,
                                                        func=self.screenHandler, data="RefProgram", disabled=True)

        moneymove_grid = MDGridLayout(cols=2, spacing=50, size_hint_y=.5)
        self.TopUp_button = elements.IconCard(text="Пополнить", image_path='images/top-up.png', data="TopUp",
                                              func=self.screenHandler, disabled=True)
        self.Withdraw_button = elements.IconCard(text="Вывести", image_path='images/withdrawal.png', data="Withdraw",
                                                 func=self.screenHandler, disabled=True)
        moneymove_grid.add_widget(self.TopUp_button)
        moneymove_grid.add_widget(self.Withdraw_button)

        grid.add_widget(self.title)
        grid.add_widget(self.ProfileCard_instance)
        grid.add_widget(MDSeparator())
        grid.add_widget(moneymove_grid)
        grid.add_widget(self.OpenDeposit_button)
        grid.add_widget(self.MyDeposits_button)
        grid.add_widget(self.ProfitCalc_button)
        grid.add_widget(self.RefferalProgram_button)
        grid.add_widget(MDBoxLayout())

        self.add_widget(grid)

        self.ID = None
        self.REQUEST_ERR_COUNT = 0
        self.IS_INIT = False

    def screenHandler(self, data, *args):
        if data == "ProfitCalc":
            elements.change_screen(self.screen_manager, "ProfitCalc")
        elif data == "OpenDeposit":
            elements.change_screen(self.screen_manager, "Packs")
        elif data == "MyDeposits":
            elements.change_screen(self.screen_manager, "MyPacks")
        else: print(data)

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.start_animate_all, 0)
        Clock.schedule_once(self.grab_my_id)
        Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                      req_body=json.dumps({'method': 'MM_lookup', 'id': self.ID}),
                                                      on_success=self.success_mm,
                                                      on_error=self.error_mm,
                                                      timeout=appconf.REQUEST_TIMEOUT,
                                                      ca_file=certifi.where()), 0)
        if self.IS_INIT:
            Clock.schedule_once(self.stop_animate_all, 0)

        # with self.canvas.after:
        #     Color(1, 1, 1, 1)
        #     self.rect = RoundedRectangle(pos=(self.width / 2, -self.height), radius=[40, 40, 40, 40],
        #                                  source='images/load_yellow.gif')

    def on_leave(self, *args):
        Clock.schedule_once(self.stop_animate_all, 0)

    # def on_touch_down(self, touch):
    #     self.start_touch_y = touch.y
    #     super(MainMenuScreen, self).on_touch_down(touch)
    #
    # def on_touch_up(self, touch):
    #     super(MainMenuScreen, self).on_touch_up(touch)
    #     Animation(pos=(self.width / 2, self.height), duration=.2).start(self.rect)
    #
    # def on_touch_move(self, touch):
    #     super(MainMenuScreen, self).on_touch_move(touch)
    #     if (self.start_touch_y - touch.y) >= 600:
    #         self.rect.pos = (self.width / 2, touch.y + 600)

    def success_mm(self, *args):
        r = json.loads(args[-1])
        Clock.schedule_once(self.stop_animate_all, 0)
        self.ProfileCard_instance.email_label.text = r['email']
        self.ProfileCard_instance.balance_deposits_label.text = f"Баланс: [font=fonts/MS_Bold]{dt.MoneyData(amount=r['balance']).AM_TEXT}[/font]\n" \
                                                                f"Активные вклады: [font=fonts/MS_Bold]{r['open_packs']}[/font]"
        self.OpenDeposit_button.disabled = False
        self.MyDeposits_button.disabled = False
        self.ProfitCalc_button.disabled = False
        self.RefferalProgram_button.disabled = False
        self.TopUp_button.disabled = False
        self.Withdraw_button.disabled = False
        self.IS_INIT = True

    def error_mm(self, *args):
        self.REQUEST_ERR_COUNT += 1
        if self.REQUEST_ERR_COUNT >= appconf.REQUEST_ERR_COUNTOUT:
            NETWORK_ERR_POPUP = MDDialog(type="custom", content_cls=elements.ERRPopupFilling())
            NETWORK_ERR_POPUP.open()
        else:
            Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                      req_body=json.dumps({'method': 'MM_lookup', 'id': self.ID}),
                                                      on_success=self.success_mm,
                                                      on_error=self.error_mm,
                                                      timeout=appconf.REQUEST_TIMEOUT,
                                                      ca_file=certifi.where()), 0)

    def grab_my_id(self, *args):
        cursor = sqlite3.connect(appconf.LOCAL_DB_FILENAME).cursor()
        MY_ID = cursor.execute("SELECT my_id FROM data").fetchone()
        if MY_ID:
            self.ID = MY_ID[0]

    def start_animate_all(self, *args):
        animations.load_animation().start(self.ProfileCard_instance)
        animations.load_animation().start(self.OpenDeposit_button)
        animations.load_animation().start(self.MyDeposits_button)
        animations.load_animation().start(self.ProfitCalc_button)
        animations.load_animation().start(self.RefferalProgram_button)
        animations.load_animation().start(self.TopUp_button)
        animations.load_animation().start(self.Withdraw_button)

    def stop_animate_all(self, *args):
        Animation.stop_all(self.ProfileCard_instance)
        Animation.stop_all(self.OpenDeposit_button)
        Animation.stop_all(self.MyDeposits_button)
        Animation.stop_all(self.ProfitCalc_button)
        Animation.stop_all(self.RefferalProgram_button)
        Animation.stop_all(self.TopUp_button)
        Animation.stop_all(self.Withdraw_button)

        self.ProfileCard_instance.opacity = 1
        self.OpenDeposit_button.opacity = 1
        self.MyDeposits_button.opacity = 1
        self.ProfitCalc_button.opacity = 1
        self.RefferalProgram_button.opacity = 1
        self.TopUp_button.opacity = 1
        self.Withdraw_button.opacity = 1

    class ProfileCard(MDCard):
        def __init__(self):
            super().__init__()
            self.size_hint_y = 1.5
            self.md_bg_color = palette.blued_gray_main_rgba
            self.radius = appconf.CARD_RADIUS
            main_grid = MDGridLayout(cols=2, padding=50)
            text_grid = MDGridLayout(cols=1, rows=4)
            nickname_grid = MDGridLayout(cols=2, rows=1, spacing=30, size_hint_y=.1)

            self.email_label = bfont.MSFont(text='Загрузка...', size='20sp', style='Bold', size_hint_y=.1)
            # edit_nick = Image(source='images/pen.png', allow_stretch=True, size_hint=[.05, .05],
            #                   pos_hint={'center_x': .1, 'center_y': .5})
            self.balance_deposits_label = bfont.MSFont(text='',
                                                       size='20sp', size_hint_y=.2)

            nickname_grid.add_widget(self.email_label)
            # nickname_grid.add_widget(edit_nick)

            text_grid.add_widget(nickname_grid)
            text_grid.add_widget(MDBoxLayout(size_hint_y=.1))
            text_grid.add_widget(self.balance_deposits_label)

            self.icon = Image(source='images/profile.png', allow_stretch=True, size_hint_x=.2)

            main_grid.add_widget(text_grid)
            main_grid.add_widget(self.icon)

            self.add_widget(main_grid)

# class TestApp(MDApp):
#     def build(self):
#         sm = MDScreenManager()
#         sm.add_widget(MainMenuScreen(sm))
#         # TEST
#         Window.size = (350, 650)
#         sm.current = "MainMenu"
#         return sm
#
#
# TestApp().run()
