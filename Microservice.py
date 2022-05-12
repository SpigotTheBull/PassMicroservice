import os
import hashlib
from time import *

# Repository of username and passwords, usernames are the key, passwords are the value
user_repo = {}

while True:
    sleep(1.0)
    f = open('new_username.txt', 'r+')
    g = open('new_password.txt', 'r+')
    username = f.readline()
    password = g.readline()
    if username != 'Success!' and username != '' and password != '':
        # This is a completely randomized salt that is within the range of 32 bytes
        # This makes using brute force/rainbow tables harder to implement
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        user_repo[username] = {
            'salt': salt,
            'key': key
        }
        f.truncate(0)
        f.seek(0)
        f.write('Success!')
        g.truncate(0)
        g.seek(0)
        g.write('Success!')
    f.close()
    g.close()

    f_new = open('verify_user.txt', 'r+')
    g_new = open('verify_password.txt', 'r+')
    verify_username = f_new.readline()
    verify_password = g_new.readline()
    if verify_username != '' and verify_username != 'Username does not exist!' and \
            verify_username != 'Password verified!' and verify_username != 'Incorrect password!' and \
            verify_password != '':
        f_new.truncate(0)
        f_new.seek(0)
        if user_repo.get(str(verify_username)) is None:
            f_new.write('Username does not exist!')
            f_new.close()
            g_new.close()
        else:
            verify_salt = user_repo[verify_username]['salt']
            new_key = hashlib.pbkdf2_hmac('sha256', verify_password.encode('utf-8'), verify_salt, 100000)
            if new_key == user_repo[verify_username]['key']:
                f_new.write('Password verified!')
            else:
                f_new.write('Incorrect password!')
            f_new.close()
            g_new.close()
    else:
        f_new.close()
        g_new.close()
