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
import certifi
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
import elements
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivy.utils import platform
import palette
import animations
import appconf


class EntryPoint(MDScreen):
    def __init__(self, screen_manager):
        super(EntryPoint, self).__init__()
        self.name = "EntryPoint"
        self.scr = screen_manager

        grid = MDGridLayout(cols=1)
        self.ENTRY_LOAD = MDCard(md_bg_color=palette.blued_gray_main_rgba)
        grid.add_widget(self.ENTRY_LOAD)
        self.ID = None

    def on_enter(self, *args):
        Clock.schedule_once(lambda *a: UrlRequest(url="https://raw.githubusercontent.com/aivythere/vw/main/server",
                                                  on_success=self.is_db_init,
                                                  on_error=self.error_serverip,
                                                  timeout=appconf.REQUEST_TIMEOUT,
                                                  ca_file=certifi.where()), 0)
        animations.load_animation().start(self.ENTRY_LOAD)

    def on_leave(self, *args):
        Animation.stop_all(self.ENTRY_LOAD)

    def is_db_init(self, *args):
        r = args[-1].replace('\n', '')
        if platform != "macosx":
            appconf.SERVER_DOMAIN = f"http://{r}/"
            print(f"IP UPDATED (osx) {appconf.SERVER_DOMAIN}")
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
                print(f"entry requested | ID: {self.ID} | PLATFORM: {platform} | IP: {appconf.SERVER_DOMAIN}")
            else: elements.change_screen(self.scr, "Login")
        except sqlite3.OperationalError:
            cursor.execute(appconf.DB_CREATION_QUERY)
            elements.change_screen(self.scr, "Login")
        except Exception as e:
            print("unexpected: (entrypoint is_db_init)", e)

    def error_serverip(self, *args):
        Clock.schedule_once(lambda *a: UrlRequest(url="https://raw.githubusercontent.com/aivythere/vw/main/server",
                                                  on_success=self.success_serverip,
                                                  on_error=self.error_serverip,
                                                  timeout=appconf.REQUEST_TIMEOUT,
                                                  ca_file=certifi.where()), 0)
        print("ERROR GETTING IP")

    def success_entrypoint(self, *args):
        print("ENTRY SUCCESS")
        r = json.loads(args[-1])

        if r['state'] == "LOGGED":
            elements.change_screen(self.scr, "MainMenu")
            return
        elements.change_screen(self.scr, "Login")
        # TODO Удаление экранов, если например уже залогинен
        #      self.scr.get_screen("Login", "EntryPoint", "CodeInput") delete

    def error_entrypoint(self, *args):
        print(f'error ENTRYPOINT | self.id: {self.id}', args)


