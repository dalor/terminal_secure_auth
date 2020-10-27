import npyscreen
from .service import create_password, Alert

def alert(text):
    npyscreen.notify_confirm(text, title='ALERT !!!', form_color='DANGER')

def info(text):
    npyscreen.notify_confirm(text, title='INFO')

def check_passwords(password, repeated_password, check=False):
    try:
        return create_password(password, repeated_password, check=check)
        info('User password is updated')
    except Alert as alert_:
        alert(alert_.text)