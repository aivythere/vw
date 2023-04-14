from kivymd.uix.card import MDCard

import animations
import bfont
import palette
from kivy.clock import Clock
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.app import MDApp


class Splash(MDCard):
    def __init__(self):
        super(Splash, self).__init__()
        self.md_bg_color=palette.white_rgba

        bl = MDBoxLayout(orientation='vertical', spacing=50, padding=50)
        self.Load_animation = Image(source='images/load_yellow.gif', size_hint_x=.5, allow_stretch=True,
                                    anim_delay=0.04, pos_hint={'center_x': .5, 'center_y': .5})
        self.Brand_label = bfont.MSFont(text='Genesis Invest\n'
                                             '[font=fonts/MS_Medium][size=20sp]'
                                             'Инвестируй с ИИ'
                                             '[/font][/size]', style='XBold', size='50sp',
                                        valign='top', halign='center')

        bl.add_widget(self.Load_animation)
        bl.add_widget(self.Brand_label)
        self.add_widget(bl)
#
# class LakeApp(MDApp):
#
#     def build(self):
#         sm = MDScreenManager()
#         sm.add_widget(SplashScreen())
#
#         return sm
# LakeApp().run()