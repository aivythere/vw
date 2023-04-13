
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest

import animations
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard, MDSeparator
import regex
import bfont
import palette
import appconf
import certifi
import json
import elements


class LoginScreen(MDScreen):
    def __init__(self, screen_manager, otp_screen_reload):
        super(LoginScreen, self).__init__()
        self.name = "Login"
        self.screen_manager = screen_manager
        self.otp_screen_reload = otp_screen_reload
        grid = MDGridLayout(cols=1, spacing=50, padding=[50, 300, 50, 300])

        self.title = bfont.MSFont(text='[size=30sp][color=000000]Зарегистрироваться[/color][/size]'
                                       '[size=15sp][color=868686]\nили войти[/size][/color]',
                                  style='Bold', size_hint_y=.3)
        self.EmailInput_instance = elements.BetterTextInput(on_text_change=lambda *a: ...,
                                                             pic_filename='emailinputat.png',
                                                             font_size=20,
                                                             placeholder='E-mail')
        self.continue_button = MDCard(
            bfont.MSFont(text="Продолжить", style="Bold", halign='center'),
            padding=[40, 20, 40, 20],
            size_hint_y = .25,
            md_bg_color = palette.blued_gray_main_rgba,
            radius=appconf.CARD_RADIUS,
            ripple_behavior = True,
            ripple_alpha = .2
        )
        self.continue_button.bind(
            on_release = self.register_attemp
        )
        #separator
        grid.add_widget(self.title)
        grid.add_widget(self.EmailInput_instance)
        grid.add_widget(self.continue_button)
        grid.add_widget(MDSeparator())
        grid.add_widget(self.LowerButtons())
        self.add_widget(grid)

        self.REQUEST_ERR_COUNT = 0
        self.EMAIL = None

    def success_exist(self, *args):
        r = json.loads(args[-1])
        print(f'success_exist data: {r}')
        self.continue_button.disabled = False
        self.otp_screen_reload(email=self.EMAIL)
        elements.change_screen(self.screen_manager, "CodeInput")

    def _is_email(self, email):
        res = regex.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email)
        return bool(res)

    def error_exist(self, *args):
        print(f'err_exist data: {args}')

        self.REQUEST_ERR_COUNT += 1
        if self.REQUEST_ERR_COUNT >= appconf.REQUEST_ERR_COUNTOUT:
            NETWORK_ERR_POPUP = MDDialog(type="custom", content_cls=elements.ERRPopupFilling())
            NETWORK_ERR_POPUP.open()
            self.continue_button.disabled = False
        else:
            Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                      req_body=json.dumps({"method": "GET_OTP", "email": self.EMAIL}),
                                                      on_success=self.success_exist, on_error=self.error_exist,
                                                      timeout=appconf.REQUEST_TIMEOUT,
                                                      ca_file=certifi.where()), appconf.REQUEST_RETRY_INTERVAL)

    def register_attemp(self, *args):
        self.EMAIL = self.EmailInput_instance.text_field.text
        if self._is_email(self.EMAIL):
            self.continue_button.disabled = True
            Clock.schedule_once(lambda *a:  UrlRequest(url=appconf.SERVER_DOMAIN,
                    req_body=json.dumps({"method": "GET_OTP", "email": self.EMAIL}),
                    on_success=self.success_exist, on_error=self.error_exist,
                    timeout=appconf.REQUEST_TIMEOUT,
                    ca_file=certifi.where()), 0)
        else:
            animations.card_change_bg(palette.card_unavailable_red).start(self.EmailInput_instance)

    class LowerButtons(MDBoxLayout):
        def __init__(self):
            super().__init__()
            self.orientation = 'vertical'
            self.spacing = 30
            self.size_hint_y = .7
            self.google_login_button = MDCard(
                    MDGridLayout(
                        Image(source='images/google_icon.png', size_hint_x=.2),
                        bfont.MSFont(text="Войти с Google", style="Bold", halign='center', size='20sp'),
                        cols=2, rows=1, spacing=10
                    ),
                padding=[40, 20, 40, 20],
                size_hint = [.7, .1],
                md_bg_color=palette.blued_gray_main_rgba,
                radius=40,
                ripple_behavior=True,
                pos_hint={'center_x': .5, 'center_y': .6},
                ripple_alpha=.2
            )
            self.vk_login_button = MDCard(
                MDGridLayout(
                    Image(source='images/vk_icon.png', size_hint_x=.2),
                    bfont.MSFont(text="Войти с VK", style="Bold", halign='center', size='20sp'),
                    cols=2, rows=1, spacing=10
                ),
                padding=[40, 20, 40, 20],
                size_hint=[.5, .1],
                md_bg_color=palette.blued_gray_main_rgba,
                radius=40,
                ripple_behavior=True,
                pos_hint={'center_x': .5, 'center_y': .4},
                ripple_alpha=.2
            )
            self.add_widget(self.google_login_button)
            self.add_widget(self.vk_login_button)


# class TestApp(MDApp):
#     def build(self):
#         sm = MDScreenManager()
#         sm.add_widget(LoginScreen(sm))
#         # TEST
#         Window.size = (350, 650)
#         sm.current = "Login"
#         return sm
#
#
# TestApp().run()