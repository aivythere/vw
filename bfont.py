from kivymd.uix.label import MDLabel
import appconf
from kivy.metrics import dp, sp


class MSFont(MDLabel):
    def __init__(self, text: str, size="30sp", style="Medium",
                 color=appconf.PRIMARY_TEXT_COLOR, **kwargs):
        super(MSFont, self).__init__(**kwargs)
        self.text = text
        self.theme_text_color = "Custom"
        self.text_color = color
        self.font_size = sp(int(size.replace("sp", "")))
        self.font_name = f"fonts/MS_{style}"
        self.markup = True