from kivy.animation import Animation
import palette
import appconf


def change_text_color_anim(color):
    return Animation(text_color=color, duration=.1)


def slider_anim(value):
    return Animation(value=round(int(value), 2), duration=.1)


def load_animation(so=.5):
    anim = (Animation(opacity=so, duration=.4) + Animation(opacity=1, duration=.4))
    anim.repeat = True
    return anim


def card_change_bg(change_to):
    anim = Animation(md_bg_color=change_to, duration=.3) + \
           Animation(md_bg_color=palette.blued_gray_main_rgba, duration=.3)
    return anim


def change_size_anim(upscale=True):
    if upscale:
        return Animation(size_hint=[1, 1], duration=0.1)
    return Animation(size_hint=[.7, .8], duration=0.1)


def backbutton_opacity(s=.5, e=1, dur=.2):
    return Animation(opacity=s, duration=dur) + Animation(opacity=e, duration=dur)


def uplight_text(color=palette.unavailable_red):
    return Animation(text_color=color, duration=.2) + Animation(text_color=appconf.PRIMARY_TEXT_COLOR, duration=1)

def upscale_placeholder():
    anim = Animation(opacity=1, duration=.2)
    anim &= Animation(size_hint=[1, .5], duration=.2)
    return anim

def scroll_hint():
    # Y
    return Animation(scroll_y=0.7, duration=.25) + Animation(scroll_y=1, duration=.25)# + \
           # Animation(scroll_y=1.2, duration=.25) + Animation(scroll_y=1, duration=.25)