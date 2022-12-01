import socket
import sys
import io
import os

HOST = "127.0.0.1"
port = int(sys.argv[1])

DATA = ["test1", "test2", "test3"]

binary_stream = io.BytesIO()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for i, data in enumerate(DATA):
        binary_stream.seek(0)
        binary_stream.write(data.encode('ascii'))
        binary_stream.seek(0)
        stream_data = binary_stream.read()

        s.sendto(stream_data, (HOST, port))
        print(f"Sent #{i+1} datagram")
