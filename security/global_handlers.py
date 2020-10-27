from curses import KEY_F1
from .utils import info

def register(self):
    self.add_handlers({
        KEY_F1: show_info,
        "^X": lambda _: logout(self)
    })

def show_info(_):
    info('''This lab is made by Duda Volodimir IS-73

Controls:
    F1 - show this info
    CTRL + X - logout''')

def logout(self):
    self.parentApp.switchForm('MAIN')
