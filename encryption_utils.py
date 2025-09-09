from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()
print(Fernet.generate_key().decode())

def get_cipher(key):
    return Fernet(key)

def encrypt_file(file_bytes, key):
    cipher = get_cipher(key)
    return cipher.encrypt(file_bytes)

def decrypt_file(encrypted_bytes, key):
    cipher = get_cipher(key)
    return cipher.decrypt(encrypted_bytes)
