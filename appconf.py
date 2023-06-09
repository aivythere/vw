from kivy.metrics import sp
from kivymd.uix.transition import MDSlideTransition

import palette

APP_THEME = "Light"
APP_PRIMARY_PALLETE = "Blue"
APP_TITLE = "Genesis Invest"
PRIMARY_TEXT_COLOR = palette.white_rgba if APP_THEME == "Dark" else palette.black_rgba
CARD_RADIUS = sp(20)
OVERALL_PADDING = [50, 10, 50, 50]
DEFAULT_TRANSITION = MDSlideTransition(duration=.2)
APP_SIZE = 480, 1080
SCREEN_BACKFUNC_STRUCTURE = {"MainMenu": "GOBACK", "ProfitCalc": "MainMenu", "Packs": "MainMenu",
                             "DepositScreen": "Packs", "MyPacks": "MainMenu", "Congratz": "MainMenu"}
UNBACKABLE_SCREENS = ["CodeInput", "MainMenu", "Login", "EntryPoint"]


# USER_SIDE
SERVER_DOMAIN = 'http://localhost:8000/'
LOCAL_DB_FILENAME = 'local.db'
REQUEST_ERR_COUNTOUT = 10
REQUEST_TIMEOUT = 10
REQUEST_RETRY_INTERVAL = 0
PLACEHOLDER_LIST = ['Имя', 'E-mail', 'Телефон', 'Код', 'Сумма вклада']
DOMAIN = 'nodomain.com' #  'prettycloneisnt.com'
DB_CREATION_QUERY = """
CREATE TABLE "data" (
	"my_id"	INTEGER,
	PRIMARY KEY("my_id")
)
"""
# ENCRYPTION_KEY =

# TODO ВСЕ КОММЕНТАРИИ НА УКРАИНСКОМ