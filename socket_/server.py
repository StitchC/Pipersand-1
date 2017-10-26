import socket
import time


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serversocket.bind(('', 4000)) # 'localhost'
serversocket.listen(1)


while True:
    serversocket.settimeout(10)
    connection, address = serversocket.accept()
    connection.settimeout(10)
    print(address)
    connection.send(b'welcome connect')

    msg = 'init'
    while len(msg):
        try:
            msg = connection.recv(30)
            print(msg)
            if msg == b'TIME':
                now = time.ctime()
                connection.send(now.encode())
            elif msg == b'IP':
                connection.send(address[0].encode() + bytes(address[1]))
            elif msg == b'EXIT':
                connection.close()
        except socket.timeout:
            print("time out")
            break
