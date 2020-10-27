import npyscreen
from .service import check_user_auth, Alert
from .utils import alert
from .global_handlers import register

class Login(npyscreen.Form):

    DEFAULT_LINES      = 6
    DEFAULT_COLUMNS    = 50

    MAX_TRIES = 3

    def create(self):

        self.user = None
        self.tries = 0
        self.center_on_display()
        self.login = self.add(npyscreen.TitleText, name='Login')
        self.password = self.add(npyscreen.TitlePassword, name='Password')

        register(self)

    def afterEditing(self):
        try:
            self.user = check_user_auth(self.login.value, self.password.value)
            self.login.value = ''
            self.password.value = ''
            if self.user.is_admin:
                self.parentApp.switchForm('admin')
            else:
                self.parentApp.switchForm('guest')
        except Alert as alert_:
            if self.tries < self.MAX_TRIES:
                alert(alert_.text)
                self.tries += 1
            else:
                exit(0)
