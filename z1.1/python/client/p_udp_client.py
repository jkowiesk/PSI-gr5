import socket
import sys
import io

HOST = "127.0.0.1"
port = int(sys.argv[1])

DATA = ["test1".encode("ascii"), "test2".encode("ascii"), "test3".encode("ascii")]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for i, data in enumerate(DATA):
        s.sendto(data, (HOST, port))
        print(f"Sent #{i+1} datagram")