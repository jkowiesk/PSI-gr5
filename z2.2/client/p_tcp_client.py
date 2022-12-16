import socket
import sys

if len(sys.argv) < 3:
    print("No server adrress or port was given")
    print("Setting default values: a: 172.18.0.2, p: 8000")
    localIP = '0.0.0.0'
    localPort = 8000
else:
    localIP = sys.argv[1]
    localPort = int(sys.argv[2])
bufferSize = 8

sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
sock.bind((localIP, localPort))
print("TCP server up and listening")

sock.listen(16)
while(True):
   # receiving name from client
    host, addr = sock.accept()
    with host:
        while(True):
            msg = host.recv(bufferSize)
            if not msg:
               break
            msg = msg.decode()
            print(msg)

    sock.close()