import json

import certifi
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
import appconf
import login_screen
import otpcode_screen
import profitcalc_screen
import mainmenu_screen
import entrypoint
import deposit_screen
import cache_manager
import packs_screen
import my_packs_screen
from kivy.utils import platform
from kivy.base import EventLoop
import elements
from kivymd.utils.set_bars_colors import set_bars_colors
import palette


# class KindaScreenManager(MDScreenManager):
#     def __init__(self):
#         super(KindaScreenManager, self).__init__()
#         self.history = []
#
#     def on_current(self, instance, value):
#         super(KindaScreenManager, self).on_current(instance, value)
#         self.current = value
#         self.history.append(value)
#         Clock.schedule_once(self.hsac, 0)
#
#     def hsac(self, *args):
#         if len(self.history) > 2:
#             self.history.pop(0)
#         cache_manager.Cache.append('Genesis', 'screen_history', self.history)
#         hs = cache_manager.Cache.get('Genesis', 'screen_history')
#         print(f"CACHE SH: {hs[0]}")

class PassiveIncomeApp(MDApp):

    def build(self):
        self.ScreenManager = MDScreenManager()
        # Window.fullscreen = True

        self.theme_cls.theme_style = appconf.APP_THEME
        self.theme_cls.primary_palette = appconf.APP_PRIMARY_PALLETE
        self.title = appconf.APP_TITLE

        # TODO if entrypoint.LOGGED = FALSE иначе нихуя не добавляем и сразу в мейн
        self.ENTRYPOINT = entrypoint.EntryPoint(self.ScreenManager)
        self.OtpCodeScreen = otpcode_screen.CodeInputScreen(self.ScreenManager)
        self.LoginScreen = login_screen.LoginScreen(self.ScreenManager, self.OtpCodeScreen.reload)
        self.ProfitCalculator = profitcalc_screen.ProfitCalculatorScreen(self.ScreenManager)
        self.MainMenuScreen = mainmenu_screen.MainMenuScreen(self.ScreenManager)
        self.DepositScreen = deposit_screen.DepositScreen(self.ScreenManager)
        self.PacksScreen = packs_screen.PacksScreen(self.ScreenManager)
        self.MyPacksScreen = my_packs_screen.MyPacksScreen(self.ScreenManager)

        self.ScreenManager.add_widget(self.ENTRYPOINT)
        self.ScreenManager.add_widget(self.LoginScreen)
        self.ScreenManager.add_widget(self.DepositScreen)
        self.ScreenManager.add_widget(self.OtpCodeScreen)
        self.ScreenManager.add_widget(self.ProfitCalculator)
        self.ScreenManager.add_widget(self.MainMenuScreen)
        self.ScreenManager.add_widget(self.PacksScreen)
        self.ScreenManager.add_widget(self.MyPacksScreen)

        cache_manager.Cache.append('Genesis', 'func_depscreen', self.DepositScreen.reload)

        self.ScreenManager.current = "EntryPoint"
        if platform == "macosx":
            Window.size = appconf.APP_SIZE
        if platform == "android":
            self.status_bar_colors()
            appconf.APP_SIZE = Window.size

        return self.ScreenManager

    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)
        Clock.schedule_once(self.hookPacks, 0)

    def hookPacks(self, *args):

        def success_pscc(*args):
            r = json.loads(args[-1])
            self.PacksScreen.create_dep_card(rdata=r)

        UrlRequest(url=appconf.SERVER_DOMAIN,
                   req_body=json.dumps({'method': 'DEPS_lookup'}),
                   on_success=success_pscc,
                   timeout=appconf.REQUEST_TIMEOUT,
                   ca_file=certifi.where())


    def status_bar_colors(self):
        set_bars_colors(
            palette.white_rgba if appconf.APP_THEME == "Light" else palette.black_rgba,  # status bar color
            palette.white_rgba if appconf.APP_THEME == "Light" else palette.black_rgba,  # navigation bar color
            "Dark" if appconf.APP_THEME == "Light" else "Light",  # icons color of status bar (opposite)
        )

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            # do what you want, return True for stopping the propagation
            if self.ScreenManager.current not in appconf.UNBACKABLE_SCREENS:
                 elements.change_screen(self.ScreenManager, appconf.SCREEN_BACKFUNC_STRUCTURE[self.ScreenManager.current],
                                        'right')
            return True


if __name__ == '__main__':
    PassiveIncomeApp().run()