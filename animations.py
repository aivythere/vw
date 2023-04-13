from kivy.animation import Animation
import palette

def change_text_color_anim(color):
    return Animation(text_color=color, duration=.1)

def slider_anim(value):
    return Animation(value=round(int(value), 2), duration=.1)

def load_animation():
    anim = (Animation(opacity=.5, duration=.4) + Animation(opacity=1, duration=.4))
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