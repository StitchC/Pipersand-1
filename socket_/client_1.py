import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 4000))
msg = s.recv(30)
print(msg)

s.send("TIME".encode())
msg = s.recv(30)
print(msg)

s.send(b"IP")
msg = s.recv(30)
print(msg)

print("Testing sleep now, please wait")
time.sleep(11)

s.close()
