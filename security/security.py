from passlib.hash import sha256_crypt

salt = 'itsmedalor'

encryptor = sha256_crypt.using(rounds=333, salt=salt, relaxed=True)

def encrypt_password(password):
    return encryptor.hash(password)


def check_encrypted_password(password, hashed):
    return encryptor.verify(password, hashed)
