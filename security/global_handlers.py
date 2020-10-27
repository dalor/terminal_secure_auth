from curses import KEY_F1
from .utils import info
from db_encoding import encrypt_sql, delete_db

def register(self):
    self.add_handlers({
        KEY_F1: show_info,
        "^X": lambda _: logout(self),
        "^E": lambda _: encrypt_sql() or delete_db() or exit(0)
    })

def show_info(_):
    info('''This lab is made by Duda Volodimir IS-73

Controls:
    F1 - show this info
    CTRL + X - logout
    CTRL + E - exit''')

def logout(self):
    self.parentApp.switchForm('MAIN')
