from cryptography.fernet import Fernet
import getpass

import LogManager


# Generate secret key for sender
def generate_sender_key():
    key = Fernet.generate_key()
    with open('Security/key.key', 'wb') as key_file:
        key_file.write(key)
    LogManager.Log("NEW SENDER KEY GENERATED")

# Generate secret key for database sql authentication
def generate_database_key():
    key = Fernet.generate_key()
    with open('Security/DBkey.key', 'wb') as key_file:
        key_file.write(key)
    LogManager.Log("NEW DATABASE KEY GENERATED (SQL)")

# Generate secret key for database windows authentication
def generate_databasewin_key():
    key = Fernet.generate_key()
    with open('Security/DBwinkey.key', 'wb') as key_file:
        key_file.write(key)
    LogManager.Log("NEW DATABASE KEY GENERATED (WIN)")

# Encrypt and save sender email credentials to a file (takes input in terminal for debug)
def save_sender_credentials():
    email = input("Enter Senders email address:")
    password = getpass.getpass("Enter Senders password: ")

    with open('Security/key.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    encrypted_email = cipher_suite.encrypt(email.encode())
    encrypted_password = cipher_suite.encrypt(password.encode())

    with open('Data/credentials.txt', 'wb') as file:
        file.write(encrypted_email + b'\n')
        file.write(encrypted_password)
    LogManager.Log("SENDERS CREDENTIALS UPDATED TO '" + email + "'")

# Encrypt and save sender email credentials to a file
def save_sender_credentials(email,password):
    with open('Security/key.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    encrypted_email = cipher_suite.encrypt(email.encode())
    encrypted_password = cipher_suite.encrypt(password.encode())

    with open('Data/credentials.txt', 'wb') as file:
        file.write(encrypted_email + b'\n')
        file.write(encrypted_password)
    LogManager.Log("SENDERS CREDENTIALS UPDATED TO '" + email + "'")

# Encrypt and save database credentials sql authentication to a file (takes input in terminal for debug)
def save_database_credentials():
    username = input("Enter database username:")
    password = getpass.getpass("Enter Senders password: ")
    host = input("Enter database host ip:")
    database = input("Enter database name:")

    with open('Security/DBkey.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    encrypted_email = cipher_suite.encrypt(username.encode())
    encrypted_password = cipher_suite.encrypt(password.encode())
    encrypted_host = cipher_suite.encrypt(host.encode())
    encrypted_database = cipher_suite.encrypt(database.encode())

    with open('Data/DBcredentials.txt', 'wb') as file:
        file.write(encrypted_email + b'\n')
        file.write(encrypted_password + b'\n')
        file.write(encrypted_host + b'\n')
        file.write(encrypted_database)

    LogManager.Log("DATABASE CREDENTIALS UPDATED (SQL)")

# Encrypt and save database credentials sql authentication to a file
def save_database_credentials(username,password,host,database):

    with open('Security/DBkey.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    encrypted_email = cipher_suite.encrypt(username.encode())
    encrypted_password = cipher_suite.encrypt(password.encode())
    encrypted_host = cipher_suite.encrypt(host.encode())
    encrypted_database = cipher_suite.encrypt(database.encode())

    with open('Data/DBcredentials.txt', 'wb') as file:
        file.write(encrypted_email + b'\n')
        file.write(encrypted_password + b'\n')
        file.write(encrypted_host + b'\n')
        file.write(encrypted_database)

    LogManager.Log("DATABASE CREDENTIALS UPDATED (SQL)")

# Decrypt and read sender email credentials from the file
def read_sender_credentials():
    with open('Security/key.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)

    with open('Data/credentials.txt', 'rb') as file:
        encrypted_email = file.readline().strip()
        encrypted_password = file.readline().strip()

    email = cipher_suite.decrypt(encrypted_email).decode()
    password = cipher_suite.decrypt(encrypted_password).decode()

    return email, password

# Decrypt and read database credentials sql authentication from the file
def read_database_credentials():
    with open('Security/DBkey.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)

    with open('Data/DBcredentials.txt', 'rb') as file:
        encrypted_user = file.readline().strip()
        encrypted_password = file.readline().strip()
        encrypted_hostname = file.readline().strip()
        encrypted_database = file.readline().strip()
    user = cipher_suite.decrypt(encrypted_user).decode()
    password = cipher_suite.decrypt(encrypted_password).decode()
    hostname = cipher_suite.decrypt(encrypted_hostname).decode()
    database = cipher_suite.decrypt(encrypted_database).decode()
    return user, password, hostname, database

# Encrypt and save database credentials windows authentication to a file (takes input in terminal for debug)
def save_database_win_credentials():
    server = input("Enter server:")
    database = input("Enter database name:")

    with open('Security/DBwinkey.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    encrypted_server = cipher_suite.encrypt(server.encode())
    encrypted_database = cipher_suite.encrypt(database.encode())

    with open('Data/DBcredentials.txt', 'wb') as file:
        file.write(encrypted_server + b'\n')
        file.write(encrypted_database)

    LogManager.Log("DATABASE CREDENTIALS UPDATED (WIN)")

# Encrypt and save database credentials windows authentication to a file
def save_database_win_credentials(server,database):

    with open('Security/DBwinkey.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)
    encrypted_server = cipher_suite.encrypt(server.encode())
    encrypted_database = cipher_suite.encrypt(database.encode())

    with open('Data/DBwincredentials.txt', 'wb') as file:
        file.write(encrypted_server + b'\n')
        file.write(encrypted_database)

    LogManager.Log("DATABASE CREDENTIALS UPDATED (WIN)")

# Decrypt and read database windows authentication credentials from the file
def read_databasewin_credentials():
    with open('Security/DBwinkey.key', 'rb') as key_file:
        key = key_file.read()
    cipher_suite = Fernet(key)

    with open('Data/DBwincredentials.txt', 'rb') as file:
        encrypted_server = file.readline().strip()
        encrypted_database = file.readline().strip()
    server = cipher_suite.decrypt(encrypted_server).decode()
    database = cipher_suite.decrypt(encrypted_database).decode()
    return server, database

#Generate connection string for windows authentication
def generate_win_string():
    credentials = read_databasewin_credentials()
    return (r'Driver=SQL Server;Server='+credentials[0]+';Database='+credentials[1]+';Trusted_Connection=yes;')


