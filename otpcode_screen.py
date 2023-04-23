import sqlite3

from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard, MDSeparator
import animations
import bfont
import palette
import appconf
import certifi
import json
import elements


class CodeInputScreen(MDScreen):
    def __init__(self, screen_manager):
        super(CodeInputScreen, self).__init__()
        self.name = "CodeInput"
        self.screen_manager = screen_manager
        grid = MDGridLayout(cols=1, padding=appconf.OVERALL_PADDING, spacing=50)
        self.title = bfont.MSFont(text='Вход в профиль', style="Bold", halign='center', size_hint_y=.1)
        self.email_label = bfont.MSFont(text='', halign='center', size='20sp', size_hint_y=.2)
        # separator
        self.code_input = elements.BetterTextInput(pic_filename='message.png',
                                                   placeholder='Код',
                                                   font_size=25)
        self.SubmitCode_instance = self.SubmitCode(self.submitCode)

        grid.add_widget(MDBoxLayout(size_hint_y=.7))
        grid.add_widget(self.title)
        grid.add_widget(self.email_label)
        grid.add_widget(MDSeparator())
        grid.add_widget(self.code_input)
        grid.add_widget(self.SubmitCode_instance)
        grid.add_widget(MDBoxLayout())

        self.add_widget(grid)

        self.CODE = None
        self.EMAIL = None
        self.PHONE = None
        self.NAME = None
        self.REQUEST_ERR_COUNT = 0

    def reload(self, email):
        self.EMAIL = email
        self.email_label.text = "Мы отправили код на\n" \
                                f"[font=fonts/MS_Bold]{self.EMAIL}[/font]"

    def finalizeReg(self, *args):
        ID = args[-1]
        def _update_db(ID):
            con = sqlite3.connect(appconf.LOCAL_DB_FILENAME)
            cur = con.cursor()
            try:
                cur.execute(f"INSERT INTO data VALUES ('{ID}');")
                con.commit()
            except sqlite3.IntegrityError:
                cur.execute(f"UPDATE data SET my_id = '{ID}';")
                con.commit()
        Clock.schedule_once(lambda *a: _update_db(ID))
        # self.screen_manager.current = "MainMenu"
        elements.change_screen(self.screen_manager, "MainMenu")
        ...

    def success_otp(self, *args):
        r = json.loads(args[-1])
        if r['response'] == "TRUE":
            Clock.schedule_once(lambda *a: self.finalizeReg(r['id']), 0 )
        else:
            animations.card_change_bg(palette.card_unavailable_red).start(self.code_input)

    def error_otp(self, *args):
        self.REQUEST_ERR_COUNT += 1
        if self.REQUEST_ERR_COUNT >= appconf.REQUEST_ERR_COUNTOUT:
            NETWORK_ERR_POPUP = MDDialog(type="custom", content_cls=elements.ERRPopupFilling())
            NETWORK_ERR_POPUP.open()
            self.SubmitCode_instance.disabled = False
        else:
            Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                  req_body=json.dumps(
                                                      {"method": "SUBMIT_OTP", "email": self.EMAIL, "otp": self.CODE}),
                                                  on_success=self.success_otp, on_error=self.error_otp,
                                                  timeout=appconf.REQUEST_TIMEOUT,
                                                  ca_file=certifi.where()), appconf.REQUEST_RETRY_INTERVAL)

    def submitCode(self, *args):
        self.CODE = self.code_input.text_field.text
        self.SubmitCode_instance.disabled = True
        Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                  req_body=json.dumps(
                                                      {"method": "SUBMIT_OTP", "email": self.EMAIL, "otp": self.CODE}),
                                                  on_success=self.success_otp, on_error=self.error_otp,
                                                  timeout=appconf.REQUEST_TIMEOUT,
                                                  ca_file=certifi.where()), 0)

    class SubmitCode(MDBoxLayout):
        def __init__(self, submitCode_func):
            super().__init__()
            self.padding = [100, 20, 100, 20]
            self.size_hint_y = .3
            self.add_widget(
                MDCard(
                    bfont.MSFont(
                        text='Войти',
                        style='Bold',
                        halign='center',
                        size='20sp'),
                    md_bg_color=palette.accent_yellow_rgba,
                    radius=appconf.CARD_RADIUS,
                    on_release=submitCode_func,
                    ripple_behavior=True
                )
            )


# class TestApp(MDApp):
#     def build(self):
#         sm = MDScreenManager()
#         sm.add_widget(sw := CodeInputScreen(sm))
#         sw.reload('niceemailtowrit@gmail.com')
#         # TEST
#         Window.size = (350, 650)
#         sm.current = "CodeInput"
#         return sm
#
#
# TestApp().run()
