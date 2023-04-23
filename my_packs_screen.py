import sqlite3
from kivy.animation import Animation
from kivy.metrics import sp
from kivy.network.urlrequest import UrlRequest
from kivymd.uix.scrollview import MDScrollView
import dt
import animations
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.card import MDCard, MDSeparator
import bfont
import palette
import appconf
import certifi
import json
import elements


class MyPacksScreen(MDScreen):
    def __init__(self, screen_manager):
        super(MyPacksScreen, self).__init__()
        self.name = "MyPacks"
        self.scr = screen_manager
        self.PACKSLISTLEN = 16

        grid = MDGridLayout(cols=1, padding=50, spacing=50)

        self.title = bfont.MSFont(text="Загрузка...", style="Bold", size_hint_y=.5)
        self.title_lo = elements.Title(self.scr, size_hint_y=.2)
        self.title_lo.add_widget(self.title)

        #separator
        self.packs_container = MDScrollView(size_hint_y=1.5)
        # TODO packs_grid.height = sp(len(количество депов) * 50 или 100)
        self.packs_grid = MDGridLayout(cols=1, spacing=30, size_hint_y=None, height=sp(400))
        self.placeholder = MDCard(md_bg_color=palette.blued_gray_main_rgba, radius=appconf.CARD_RADIUS,
                                  size_hint_y=None, height=sp(800))

        self.packs_grid.add_widget(self.placeholder)
        self.packs_container.add_widget(self.packs_grid)

        grid.add_widget(self.title_lo)
        grid.add_widget(MDSeparator())
        grid.add_widget(self.packs_container)

        self.add_widget(grid)

        self.MYID = None
        self.IS_INIT = False

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.grab_my_id, 0)
        Clock.schedule_once(self.getPacksUrlReq, 0)
        if not self.IS_INIT:
            animations.load_animation(.1).start(self.placeholder)

    def packChooseHandler(self, *args):
        item = args[0]
        _id = args[1]
        animations.load_animation(.1).start(item)


        def error_pi(*args):
            print(f'error PI {args}')

        def success_pi(self, *args):
            r = json.loads(args[-1])
            Animation.stop_all(item)
            item.opacity = 1
            PACK_INFO_POPUP = elements.PackInfoPopup(r['open_date'], r['open_sum'],
                                                     r['close_date'], r['close_sum'],
                                                     radius=[appconf.CARD_RADIUS for i in range(4)])
            PACK_INFO_POPUP.open()


        UrlRequest(url=appconf.SERVER_DOMAIN,
                   req_body=json.dumps({'method': 'get_pack', 'my_id': self.MYID, 'pack_id': _id}),
                   on_success=success_pi, on_error=error_pi,
                   timeout=appconf.REQUEST_TIMEOUT,
                   ca_file=certifi.where())

    # def scroll_handler(self, *args):
    #     print(self.packs_container.scroll_y)

    def createDepositItem(self, *args):
        if not self.IS_INIT:
            r = json.loads(args[-1])

            self.title.text = "Мои вклады"
            Animation.stop_all(self.placeholder)
            self.packs_grid.remove_widget(self.placeholder)
            if not r.get("response"):  # если ответ не содержит "response", в этом случае только если паков нет
                self.packs_grid.height = sp(len(r)*100+200)
                for i in r.keys():
                    self.packs_grid.add_widget(
                        self.DepositItem(i, f"{r[i]['period']} {elements.dayordays(r[i]['period'])}",
                                         r[i]['open_sum'], r[i]['open_date'], r[i]['close_sum'],
                                         r[i]['percent'], r[i]['payout_date'], self.packChooseHandler))
            self.IS_INIT = True
            Clock.schedule_once(lambda *a: animations.scroll_hint().start(self.packs_container), 0.5)

    def grab_my_id(self, *args):
        cursor = sqlite3.connect(appconf.LOCAL_DB_FILENAME).cursor()
        MY_ID = cursor.execute("SELECT my_id FROM data").fetchone()
        if MY_ID is not None:
            self.MYID = MY_ID[0]

    def getPacksUrlReq(self, *args):

        def error(*args):
            print('err getpacksurlreq')

        UrlRequest(url=appconf.SERVER_DOMAIN,
                   req_body=json.dumps({'method': 'packs_ov', 'my_id': self.MYID}),
                   on_success=self.createDepositItem, on_error=error,
                   timeout=appconf.REQUEST_TIMEOUT,
                   ca_file=certifi.where())


    class DepositItem(MDCard):
        def __init__(self, pack_id, period_meaning, open_price, open_date, payout, percent, payout_date,
                     func, **kwargs):
            super().__init__(**kwargs)
            self.size_hint_y = None
            self.height = sp(100)
            self.pack_id = pack_id
            self.md_bg_color = palette.blued_gray_main_rgba
            self.radius = appconf.CARD_RADIUS
            self.orf = func
            self.ripple_behavior = True
            self.ripple_alpha = .3

            grid = MDGridLayout(cols=2, spacing=30, padding=[50, 30, 50, 30])
            info_grid = MDGridLayout(rows=2)
            payout_grid = MDGridLayout(rows=3)

            self.period_op_label = bfont.MSFont(text=f"{period_meaning} [font=fonts/MS_Medium][/font]",
                                                style="Bold", size="20sp")
            self.open_date_label = bfont.MSFont(text=f"Открыт: [font=fonts/MS_Bold]{open_date}[/font]", size="15sp")

            self.payout_label = bfont.MSFont(text=f"{dt.MoneyData(payout).AM_TEXT}", style="Bold",
                                             color=palette.dark_green, size="20sp", halign="right")
            self.percent_label = bfont.MSFont(text=f"{percent}%", style="Bold", size="20sp", halign="right")
            self.payout_date_label = bfont.MSFont(text=f"~{payout_date}", style="Bold", size="15sp", halign="right")

            info_grid.add_widget(self.period_op_label)
            info_grid.add_widget(self.open_date_label)

            payout_grid.add_widget(self.payout_label)
            payout_grid.add_widget(self.percent_label)
            payout_grid.add_widget(self.payout_date_label)

            grid.add_widget(info_grid)
            grid.add_widget(payout_grid)
            self.add_widget(grid)

        def on_release(self):
            self.orf(self, self.pack_id)
#
# class TestApp(MDApp):
#     def build(self):
#         sm = MDScreenManager()
#         sm.add_widget(MyPacksScreen(sm))
#         # TEST
#         sm.current = "MyPacks"
#         return sm
#
#
# TestApp().run()