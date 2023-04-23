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
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.dialog import MDDialog
import elements
from kivymd.uix.screen import MDScreen
from kivy.utils import platform
import appconf
import splash_screen


class EntryPoint(MDScreen):
    def __init__(self, screen_manager):
        super(EntryPoint, self).__init__()
        self.name = "EntryPoint"
        self.scr = screen_manager

        self.Splash_instance = splash_screen.Splash()
        self.add_widget(self.Splash_instance)
        self.ID = None
        self.REQUEST_ERR_COUNT = 0

    def on_enter(self, *args):
        self.Splash_instance.Load_animation.anim_loop = 0
        Clock.schedule_once(lambda *a: UrlRequest(url="https://raw.githubusercontent.com/aivythere/vw/main/server",
                                                  on_success=self.is_db_init,
                                                  on_error=self.error_serverip,
                                                  timeout=appconf.REQUEST_TIMEOUT,
                                                  ca_file=certifi.where()), 0)

    def on_leave(self, *args):
        self.Splash_instance.Load_animation.anim_loop = 1
        # TODO !!!! Придумать с этим что-то !!!!
        Clock.schedule_once(lambda *a: self.scr.remove_widget(self), 1)

    def is_db_init(self, *args):
        r = args[-1].replace('\n', '')
        if platform != "macosx":
            appconf.SERVER_DOMAIN = f"http://{r}/"
            print(f"{appconf.SERVER_DOMAIN}: SERVER DOMAIN")
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
                self.scr.remove_widget(self.scr.get_screen("Login"))
                self.scr.remove_widget(self.scr.get_screen("CodeInput"))
            else:
                elements.change_screen(self.scr, "Login")
        except sqlite3.OperationalError:
            cursor.execute(appconf.DB_CREATION_QUERY)
            elements.change_screen(self.scr, "Login")

    def error_serverip(self, *args):
        print("ERROR GETTING SERVER IP")
        # TODO Получить с других мест айпи сервера

    def success_entrypoint(self, *args):
        r = json.loads(args[-1])

        if r['state'] == "LOGGED":
            elements.change_screen(self.scr, "MainMenu")
            return
        elements.change_screen(self.scr, "Login")
        # TODO Удаление экранов, если например уже залогинен
        #      self.scr.get_screen("Login", "EntryPoint", "CodeInput") delete

    def error_entrypoint(self, *args):
        self.REQUEST_ERR_COUNT += 1
        if self.REQUEST_ERR_COUNT >= appconf.REQUEST_ERR_COUNTOUT:
            NETWORK_ERR_POPUP = MDDialog(type="custom", content_cls=elements.ERRPopupFilling())
            NETWORK_ERR_POPUP.open()
        else:
            Clock.schedule_once(lambda *a: UrlRequest(url=appconf.SERVER_DOMAIN,
                                                      req_body=json.dumps({'method': 'ENTRYPOINT', 'id': self.ID}),
                                                      on_success=self.success_entrypoint, on_error=self.error_entrypoint,
                                                      timeout=appconf.REQUEST_TIMEOUT,
                                                      ca_file=certifi.where()), appconf.REQUEST_RETRY_INTERVAL)


