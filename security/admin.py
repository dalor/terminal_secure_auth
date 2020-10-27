import npyscreen
import curses
from .service import get_all_user_logins, get_user, delete_user, add_user
from .utils import check_passwords, alert, info
from .global_handlers import register

class ControlCommands(npyscreen.MultiLineAction):

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            curses.ascii.ESC: lambda _: self.parent.close()
        })

    def actionHighlighted(self, command, keypress):

        if keypress == 13:
            if command in self.parent.CONTROLS:
                self.parent.CONTROLS[command]()
    

class EditControl(npyscreen.FormBaseNew):

    DEFAULT_LINES      = 10
    DEFAULT_COLUMNS    = 50

    def create(self):

        self.user = None

        self.CONTROLS = {}

        self.center_on_display()
        
        self.controls_list = self.add(ControlCommands)

    def beforeEditing(self):

        self.update_list()

    def update_list(self):

        self.prepare_controls()
        self.controls_list.values = list(self.CONTROLS.keys())
        self.controls_list.display()

        # npyscreen.notify_confirm(self.user.password, title='INFO')

    def prepare_controls(self):
        controls = [
            ('Close', self.close)
        ]
        if self.user:
            controls.append(('Change password', self.change_password))
            controls.append(('Revoke user', self.revoke_user) if self.user.is_restricted else ('Restrict user', self.restrict_user))
            controls.append(('Promote to normal', self.promote_to_normal) if self.user.is_admin else ('Promote to admin', self.promote_to_admin))
            if not self.user.is_admin:
                controls.append(('Uncheck password', self.uncheck_password) if self.user.is_check_password else ('Check password', self.check_password))
            controls.append(('Delete user', self.delete_user))
        self.CONTROLS = dict(controls)


    def close(self):
        self.user = None
        self.parentApp.switchFormPrevious()

    def change_user_password(self, password):
        self.user.password = password

    def change_password(self):
        self.parentApp.getForm('changeUserPassword').callback = self.change_user_password
        self.parentApp.switchForm('changeUserPassword')

    def restrict_user(self):
        self.user.is_restricted = True
        self.close()

    def revoke_user(self):
        self.user.is_restricted = False
        self.close()

    def promote_to_admin(self):
        self.user.is_admin = True
        self.close()

    def promote_to_normal(self):
        self.user.is_admin = False
        self.close()

    def check_password(self):
        self.user.is_check_password = True
        self.close()

    def uncheck_password(self):
        self.user.is_check_password = False
        self.close()

    def delete_user(self):
        delete_user(self.user)
        self.close()


class UserList(npyscreen.MultiLineAction):

    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.add_handlers({
            "^C": lambda _: exit(0),
        })

    def actionHighlighted(self, login, keypress):

        if keypress == 13:
            self.parent.parentApp.getForm('editControl').user = get_user(login=login)
            self.parent.parentApp.switchForm('editControl')

class CreateUser(npyscreen.ActionForm):

    def create(self):

        self.login = self.add(npyscreen.TitleText, name='Login')
        self.is_admin = self.add(npyscreen.CheckBox, name='Is admin')
        self.password = self.add(npyscreen.TitlePassword, name='Password')
        self.repeated_password = self.add(npyscreen.TitlePassword, name='Repeated')
        self.is_check_password = self.add(npyscreen.CheckBox, name='Is check password')

    def on_ok(self):

        if get_user(login=self.login.value):
            return alert('Such user is exist')
        password = check_passwords(self.password.value, self.repeated_password.value)
        if not password:
            return
        add_user(login=self.login.value, password=password, is_admin=self.is_admin.value, is_check_password=self.is_check_password.value)
        info('User {} added'.format(self.login.value))

        self.on_cancel()

    def on_cancel(self):

        self.login.value = ''
        self.is_admin.value = False
        self.password.value = ''
        self.repeated_password.value = ''

        self.parentApp.switchFormPrevious()

class CreateUserButton(npyscreen.ButtonPress):

    def whenPressed(self):
        self.parent.parentApp.switchForm('createUser')

class UserListBox(npyscreen.BoxTitle):

    _contained_widget = UserList

class SearchBox(npyscreen.BoxTitle):

    _contained_widget = npyscreen.Textfield


class AdminPanel(npyscreen.FormBaseNew):

    def create(self):

        y, x = self.useable_space()

        self.search = self.add(SearchBox, name='Search', max_height=3, rely=1, max_width=x - 30)
        self.add(CreateUserButton, name="Create user", max_height=3, rely=2, relx=x - 22)
        self.users = self.add(UserListBox, name='Users', rely=4)

        register(self)

    def beforeEditing(self):
        self.update_list()

    def update_list(self, login=None):
        self.users.values = get_all_user_logins(login)
        self.users.display()

    def while_editing(self, _):

        self.update_list(self.search.value)

