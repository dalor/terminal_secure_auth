import npyscreen
from .utils import check_passwords

class ChangeUserPassword(npyscreen.ActionForm):

    DEFAULT_LINES      = 6
    DEFAULT_COLUMNS    = 40

    def create(self):

        self.center_on_display()

        self.password = self.add(npyscreen.TitlePassword, name='Password')
        self.repeated_password = self.add(npyscreen.TitlePassword, name='Repeated')

        self.callback = lambda password: None # Can be changed

        self.check = False

    def on_ok(self):

        password = check_passwords(self.password.value, self.repeated_password.value, check=self.check)
        if password:
            self.callback(password)
            npyscreen.notify_confirm('User password is updated', title='INFO')
            self.on_cancel()

    def on_cancel(self):

        self.callback = lambda password: None
        self.password.value = ''
        self.repeated_password.value = ''
        self.check = False

        self.parentApp.switchFormPrevious()