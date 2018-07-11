from modbus_tcp_2f85 import Gripper
import socket

print('Initializing gripper')
gripper = Gripper('10.10.10.42')
print('Sending activation request')
gripper.activate()

print('Starting TCP server')
TCP_IP = '127.0.0.1'
TCP_PORT = 1337
BUFFER_SIZE = 20
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print('Waiting for connection to TCP server')
conn, addr = s.accept()
print('Connection made!\nRunning...')

try:
    while True:
        data = conn.recv(BUFFER_SIZE)
        if data: print(data)
        if data and data == b'0\n':
            gripper.close()
        elif data and data == b'1\n':
            gripper.open()

except KeyboardInterrupt:
    conn.close()
    gripper.disconnect()
