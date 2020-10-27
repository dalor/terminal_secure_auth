import npyscreen
from .global_handlers import register

class ChangeUserPasswordButton(npyscreen.ButtonPress):

    def whenPressed(self):

        change_password = self.parent.parentApp.getForm('changeUserPassword')

        change_password.callback = self.parent.update_password
        change_password.check = self.parent.parentApp.getForm('MAIN').user.is_check_password
        self.parent.parentApp.switchForm('changeUserPassword')

class StandartPanel(npyscreen.FormBaseNew):

    def create(self):

        self.add(ChangeUserPasswordButton, name="Change password")

        register(self)

    def update_password(self, password):

        self.parentApp.getForm('MAIN').user.password = password