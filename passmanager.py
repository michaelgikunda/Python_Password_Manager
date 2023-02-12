import hashlib
from cryptography.fernet import Fernet

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_password(password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password, key

def decrypt_password(encrypted_password, key):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def store_password(service, password):
    encrypted_password, key = encrypt_password(password)
    with open("passwords.txt", "a") as f:
        f.write(service + ":" + encrypted_password.decode() + ":" + key.decode() + "\n")

def get_password(service):
    with open("passwords.txt", "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) != 3:
                continue
            if parts[0] == service:
                encrypted_password = parts[1].encode()
                key = parts[2].encode()
                return decrypt_password(encrypted_password, key)
    return "Error: The specified service has no stored password."

print("Password Manager")
print("1. Get password")
print("2. Store password")
choice = int(input("Enter your choice: "))

if choice == 1:
    service = input("Enter the name of the service: ")
    print("Retrieved password: " + get_password(service))
elif choice == 2:
    service = input("Enter the name of the service: ")
    password = input("Enter the password for '" + service + "': ")
    store_password(service, password)
    print("Password stored successfully.")
else:
    print("Invalid choice.")
