import socket
import time

ADDRESS = 'localhost'
PORT = 8034
ENCODING = 'utf-8'
req = 'get fast hex'
REQUEST_TEXT = req.encode(ENCODING)
print(REQUEST_TEXT)
RESPONCE_PREFIX = ''

BUFFER_SIZE = 100

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(100)
sock.connect((ADDRESS, PORT))


def saveData():
    try:
        if not sock.send(REQUEST_TEXT) == len(REQUEST_TEXT):
            print('Failed to send!')
            return -1
        time.sleep(10)
        return sock.recv(BUFFER_SIZE).decode(ENCODING)
    except socket.timeout:
        print('Connection timeout!')
        return -3

print('connected.')