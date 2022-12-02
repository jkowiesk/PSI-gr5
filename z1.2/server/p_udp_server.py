import socket
import sys
import os

BUFSIZE = 65536

HOST = "127.0.0.1"
port = int(sys.argv[1])


print("Will listen on ", HOST, ":", port)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, port))
    while True:
        data_address = s.recvfrom(BUFSIZE)
        data = data_address[0]
        address = data_address[1]
        print( "Message size Client:{}".format(len(data)) )
        print( "Client IP Address:{}".format(address) )
        if not data:
            print("Error in datagram?")
            break
