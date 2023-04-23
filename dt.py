from kivy.properties import StringProperty

def decorateNumberDigits(string, nofloat=False):
    if type(string) is str:
        string = string.replace(",", "")
    if not nofloat:
        return '{:,}'.format(round(float(string),2)).replace(',', ' ')
    return '{:,}'.format(int(string)).replace(',', ' ')

def st(str):
    return StringProperty(str)

class MoneyData:
    def __init__(self, amount):
        self.amount = round(float(amount), 2)
        self.AM_TEXT = f"{decorateNumberDigits(self.amount)} ₽"

