import npyscreen
from .login import Login
from .admin import AdminPanel, EditControl, CreateUser
from .change_password import ChangeUserPassword
from .standart import StandartPanel

class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", Login, "Login")
        self.addForm("admin", AdminPanel, "Admin")
        self.addForm("guest", StandartPanel, "Guest")
        self.addForm("editControl", EditControl, "Edit menu")
        self.addForm("createUser", CreateUser, "Create new user")
        self.addForm("changeUserPassword", ChangeUserPassword, "Change password")