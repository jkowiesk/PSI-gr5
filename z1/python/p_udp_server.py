import socket
import sys

BUFSIZE = 512

HOST = "127.0.0.1"
port = int(sys.argv[1])


print("Will listen on ", HOST, ":", port)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, port))
    while True:
        data_address = s.recvfrom(BUFSIZE)
        data = data_address[0]
        address = data_address[1]
        print( "Message from Client:{}".format(data.decode("ascii")) )
        print( "Client IP Address:{}".format(address) )
        if not data:
            print("Error in datagram?")
            break