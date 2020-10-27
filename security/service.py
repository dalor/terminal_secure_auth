from .db import session, User, check_table_or_create
from .security import check_encrypted_password, encrypt_password
import re

class Alert(Exception):

    def __init__(self, text):
        self.text = text

def get_user(**kwargs):
    return session.query(User).filter_by(**kwargs).first()

def check_user_auth(login, password):
    user = get_user(login=login)
    if user:
        if user.is_restricted:
            raise Alert('User is restricted')
        try:
            res = check_encrypted_password(password, user.password)
        except:
            raise Alert('Wrong encryption')
        if res:
            return user
        else:
            raise Alert('Wrong password')
    else:
        raise Alert('No such user')

def add_user(**kwargs):
    if 'password' in kwargs:
        kwargs['password'] = encrypt_password(kwargs['password'])
    user = User(**kwargs)
    session.add(user)
    return user

def get_all_user_logins(login=None):
    users = session.query(User).filter(User.login.like(login + '%')).all() if login else session.query(User).all()
    return [user.login for user in users]

def check_integers(password):
    if not re.search('[0-9]+', password):
        raise Alert('Use numbers')

def check_uppercase(password):
    if not re.search('[A-Z]+', password):
        raise Alert('Use uppercase')

def check_min_lenght(password):
    if len(password) < 8:
        raise Alert('Min password length - 8')

patterns = [check_min_lenght, check_integers, check_uppercase]

def check_password_pattern(password):
    for pattern in patterns:
        pattern(password)

def create_password(password, repeat=None, check=False):
    if check:
        check_password_pattern(password)
    if repeat is None or password == repeat:
        return encrypt_password(password)
    else:
        raise Alert('Password and repeated password are not equal')

def delete_user(user):

    session.delete(user)

def check_or_create_admin():
    check_table_or_create()
    if (not get_user(login='ADMIN')):
        add_user(login='ADMIN', password='admin', is_admin=True)
    return True

        

