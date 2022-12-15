import socket
import sys
import io

HOST = "127.0.0.1"
port = int(sys.argv[1])
DATA_SIZES = [100, 1000, 10000, 50000, 60000, 65507, 65508]

DATA = ["test1", "test2", "test3"]

binary_stream = io.BytesIO()
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    for data_size in DATA_SIZES:
        try:
            data_to_send = 'x' * data_size
            binary_stream.seek(0)
            binary_stream.write(data_to_send.encode("ascii"))
            binary_stream.seek(0)
            stream_data = binary_stream.read()
            s.sendto(stream_data, (HOST, port))
            print(f"Sent {data_size} size datagram")
        except Exception:
            print(f"Data has size of {data_size}, to big !!!")