from security.app import App
from security.service import check_or_create_admin
from computer_info import check_info

check = True

def run():
    app = App()
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