# TODO if user_logged: proceed
#      ...? if local.db is not blank = loggin_automatically
#           else:   screenmanager.add_widget(LOGINSCREEN)
#                   registrer screen
#
# TODO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# AdditionalCode:
#         Прога получает с сервера аддишнал код в энтрипоинт и выполняет его в той хуйне
#         Для оптимизации, вроде rconf или как-то так, помнишь мы прогу замеряли, это ебатьтемааа)

# TODO Если у телефона разблокирован загрузчик - НАХУЙ с приложения

import sqlite3
import json
# import os
import certifi
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
import elements
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen

import palette
import animations
import appconf


class EntryPoint(MDScreen):
    def __init__(self, screen_manager):
        super(EntryPoint, self).__init__()
        self.name = "EntryPoint"
        self.scr = screen_manager

        grid = MDGridLayout(cols=1)
        grid.add_widget(y:=MDCard(md_bg_color=palette.blued_gray_main_rgba))
        animations.load_animation().start(y)
        self.ID = None

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.is_db_init, 0)

    def success_entrypoint(self, *args):
        r = json.loads(args[-1])

        if r['state'] == "LOGGED":
            elements.change_screen(self.scr, "MainMenu")
            return
        elements.change_screen(self.scr, "Login")
        # TODO Удаление экранов, если например уже залогинен

    def error_entrypoint(self, *args):
        print('error ENTRYPOINT')

    def is_db_init(self, *args):
        con = sqlite3.connect(appconf.LOCAL_DB_FILENAME)
        cursor = con.cursor()
        try:
            dbresp = cursor.execute("SELECT my_id FROM data").fetchone()
            if dbresp:
                self.ID = dbresp[0]
                Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                          req_body=json.dumps({'method': 'ENTRYPOINT', 'id': self.ID}),
                                                          on_success=self.success_entrypoint,
                                                          on_error=self.error_entrypoint,
                                                          timeout=appconf.REQUEST_TIMEOUT,
                                                          ca_file=certifi.where()), 0)
            else: elements.change_screen(self.scr, "Login")
        except sqlite3.OperationalError:
            cursor.execute(appconf.DB_CREATION_QUERY)
            elements.change_screen(self.scr, "Login")

    # def is_logged(self, *args):
    #     UrlRequest()
    #     Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
    #                                               req_body=json.dumps({'method': 'ENTRYPOINT', 'id': self.ID}),
    #                                               on_success=self.success_entrypoint, on_error=self.error_entrypoint,
    #                                               timeout=appconf.REQUEST_TIMEOUT,
    #                                               ca_file=certifi.where()), 0)

#
# class LakeApp(MDApp):
#     def build(self):
#         self.title = "ENTRYPOINT"
#         sm = MDScreenManager()
#         sw = EntryPoint(sm)
#         sm.add_widget(sw)
#         sm.current = "EntryPoint"
#         return sm
#
# LakeApp().run()