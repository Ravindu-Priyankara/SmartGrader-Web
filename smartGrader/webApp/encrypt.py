from cryptography.fernet import Fernet

# Generate a key for encryption and decryption
def generate_key():
    return Fernet.generate_key()

# Initialize a Fernet symmetric key
key = generate_key()
cipher_suite = Fernet(key)

# Encrypt data
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode())

# Decrypt data
def decrypt_data(encrypted_data):
    decrypted_data = []
    for data in encrypted_data:
        decrypted_data.append(cipher_suite.decrypt(data).decode())
    return decrypted_data