from kivy.clock import Clock
from kivy.uix.screenmanager import NoTransition, FadeTransition
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
import appconf
import login_screen
import otpcode_screen
import profitcalc_screen
import mainmenu_screen
import entrypoint
import deposit_screen
import cache_manager
import packs_screen


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
        # TODO Entrypoint
        self.ScreenManager = MDScreenManager()

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

        self.ScreenManager.add_widget(self.ENTRYPOINT)
        self.ScreenManager.add_widget(self.LoginScreen)
        self.ScreenManager.add_widget(self.DepositScreen)
        self.ScreenManager.add_widget(self.OtpCodeScreen)
        self.ScreenManager.add_widget(self.ProfitCalculator)
        self.ScreenManager.add_widget(self.MainMenuScreen)
        self.ScreenManager.add_widget(self.PacksScreen)

        cache_manager.Cache.append('Genesis', 'func_depscreen', self.DepositScreen.reload)

        self.ScreenManager.current = "EntryPoint"

        return self.ScreenManager


if __name__ == '__main__':
    PassiveIncomeApp().run()