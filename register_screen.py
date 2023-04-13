import json
import sqlite3

from kivy.core.window import Window

import regex
import certifi
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard
import bfont
import palette
import elements
import appconf


class RegisterScreen(MDScreen):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        self.name = 'LoginStep2'
        grid = MDGridLayout(cols=1, padding=30, spacing=appconf.OVERALL_PADDING)

        self.title = bfont.MSFont(text='Регистрация', halign='left', size_hint_y=.1, style='Bold')
        self.undertitle = bfont.MSFont(text='Почти готово, введите \nоставшиеся данные', halign='left',
                                       size='20sp', size_hint_y=.2)
        self.name_input = elements.BetterTextInput(
            on_text_change=lambda *a: ...,
            pic_filename='nameinput.png',
            placeholder='Имя',
            size_hint_y=.7,
            font_size=20

        )
        self.phone_input = elements.BetterTextInput(
            on_text_change=lambda *a: ...,
            pic_filename='phone_icon.png',
            placeholder='Телефон',
            size_hint_y=.7,
            font_size=20,
            input_filter='int'
        )
        self.submit_reg_button = self.SubmitRegButton(self.submitRegister)

        grid.add_widget(self.title)
        grid.add_widget(self.undertitle)
        grid.add_widget(self.name_input)
        grid.add_widget(self.phone_input)
        grid.add_widget(self.submit_reg_button)
        grid.add_widget(MDBoxLayout(size_hint_y=.5))

        self.add_widget(grid)

        self.EMAIL = None
        self.REQUEST_ERR_COUNT = 0

    def log_in(self, id, hash, *args):
        con = sqlite3.connect(appconf.LOCAL_DB_FILENAME)
        cur = con.cursor()
        cur.execute(f"UPDATE data SET my_id = '{id}', session_hash = '{hash}';")
        con.commit()

    def loadS2(self, email):
        self.EMAIL = email

    def _is_email(self, email):
        res = regex.match(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email)
        return bool(res)

    def success_reg(self, *args):
        r = json.loads(args[-1])
        if r['response'] == 'ALR_REG':
            Clock.schedule_once(lambda *a: self.log_in(r['id'], r['hash']), 0)
        elif r['response'] == "SUCCESS":
            Clock.schedule_once(lambda *a: self.log_in(r['id'], r['hash']), 0)

    def error_reg(self, *args):
        self.REQUEST_ERR_COUNT += 1
        if self.REQUEST_ERR_COUNT >= appconf.REQUEST_ERR_COUNTOUT:
            NETWORK_ERR_POPUP = MDDialog(type="custom", content_cls=elements.ERRPopupFilling())
            NETWORK_ERR_POPUP.open()
        else:
            Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                      req_body=json.dumps({"method": "REGISTER", "email": self.EMAIL,
                                                                           "phone": self.NUMBER, "name": self.NAME}),
                                                      on_success=self.success_reg, on_error=self.error_reg,
                                                      timeout=appconf.REQUEST_TIMEOUT,
                                                      ca_file=certifi.where()), appconf.REQUEST_RETRY_INTERVAL)

    def _is_valid_phonenum(self, number):
        res = regex.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$',
                          number)
        return bool(res)

    def submitRegister(self, *args):
        if self._is_valid_phonenum(self.phone_input.text_field.text) and self.name_input.text_field.text != '':
            self.PHONE = self.phone_input.text_field.text
            self.NAME = self.name_input.text_field.text
            # phone = self.NUMBER
            Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                    req_body=json.dumps({"method": "REGISTER", "email": self.EMAIL, "phone": self.NUMBER, "name": self.NAME}),
                    on_success=self.success_reg, on_error=self.error_reg,
                    timeout=appconf.REQUEST_TIMEOUT,
                    ca_file=certifi.where()), 0)

    class SubmitRegButton(MDBoxLayout):
        def __init__(self, submitRegister_func):
            super().__init__()
            self.padding = [100, 0, 100, 0]
            self.size_hint = [.5, .2]
            self.add_widget(
                MDCard(
                    bfont.MSFont(text='Завершить', style='Bold', halign='center', size='20sp'),
                    md_bg_color=palette.accent_yellow_rgba,
                    radius=appconf.CARD_RADIUS,
                    on_release=submitRegister_func,
                    ripple_behavior=True
                )
            )



class LakeApp(MDApp):
    def build(self):
        self.title = "LOGINSCREENSTEP2"
        sm = MDScreenManager()
        sw = RegisterScreen()
        sm.add_widget(sw)
        sw.loadS2('penis@gmail.com')
        # TEST
        Window.size = (350, 650)
        sm.current = "LoginStep2"
        return sm

LakeApp().run()