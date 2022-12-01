import socket
import sys
import io
import os


HOST = os.environ.get('HOSTNAME')
port = int(sys.argv[1])

DATA = ["test1".encode("ascii"), "test2".encode("ascii"), "test3".encode("ascii")]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for i, data in enumerate(DATA):
        s.sendto(data, (HOST, port))
        print(f"Sent #{i+1} datagram")
        