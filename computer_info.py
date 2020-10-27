from win32api import GetSystemMetrics
import shutil
import platform

filename = "super.key"

from passlib.hash import sha256_crypt

encryptor = sha256_crypt.using(rounds=1000, relaxed=True)

def encrypt(text):
    return encryptor.hash(text)

def check_encrypted(text, hashed):
    return encryptor.verify(text, hashed)

disc_count = 1
mouse_count_buttons = 2
screen_resolution = (GetSystemMetrics(0), GetSystemMetrics(1))
total, used, free = shutil.disk_usage("/")
processor = platform.processor()

def get_info():
    return "Mouse buttons: {}\nScreen width: {}\nDiscs: {}\nTotal disc size: {}\nProcessor: {}".format(
        mouse_count_buttons,
        screen_resolution[0],
        disc_count,
        total,
        processor
    )

def check_info():
    try:
        with open(filename, 'r') as f:
            if check_encrypted(get_info(), f.read()):
                return True
            else:
                return False
    except:
        return False

def save_info():
    with open(filename, 'w') as f:
        f.write(encrypt(get_info()))

if __name__ == "__main__":
    print(get_info())