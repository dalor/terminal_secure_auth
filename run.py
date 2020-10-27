from security.app import App
from security.service import check_or_create_admin
from computer_info import check_info
from db_encoding import decrypt_sql

check = False

def run():
    app = App()
    decrypt_sql()
    check_or_create_admin()
    app.run()

if __name__ == '__main__':
    if check:
        if check_info():
            run()
        else:
            print("Please, reinstall programm")
            input()
    else:
        run()