from cryptography.fernet import Fernet
import os

admin_key_filename = "admin.key"

db_filename = "DB.sql"
db_encrypted_filename = "DB.ensql"

def get_admin_key():
    with open(admin_key_filename, 'rb') as f:
        return f.read()

def get_cipher():
    key = get_admin_key()
    try:
        fernet = Fernet(key)
    except:
        key = Fernet.generate_key()
        with open(admin_key_filename, 'wb') as f:
            return f.write(key)
        fernet = Fernet(key)
    return fernet

def encrypt(text):
    cipher = get_cipher()
    return cipher.encrypt(text)

def decrypt(data):
    cipher = get_cipher()
    return cipher.decrypt(data)

def decrypt_sql():
    with open(db_encrypted_filename, 'rb') as enf:
        with open(db_filename, 'wb') as f:
            f.write(decrypt(enf.read()))


def encrypt_sql():
    with open(db_encrypted_filename, 'wb') as enf:
        with open(db_filename, 'rb') as f:
            enf.write(encrypt(f.read()))

def delete_db():
    os.remove(db_filename)

if __name__ == "__main__":
    encrypt_sql()
    # decrypt_sql()

