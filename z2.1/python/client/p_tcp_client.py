import socket
import argparse
from random import choices
import string
from time import sleep

def generate_data(size):
    rand_str = ''.join(choices(string.ascii_letters, k=size))
    return str.encode(rand_str)

DATA_SIZE = 2

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server_name", help="Server's name")
    parser.add_argument("server_port", help="Server's port")
    parser.add_argument("message", help="Server's port")

    args = parser.parse_args()

    server_name = args.server_name
    server_port = int(args.server_port)
    message = str.encode(args.message)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("calling connect()")
        s.connect((server_name, server_port))
        print("after connect()\n")

        while True:
            # data = generate_data(64)
            data = message
            s.send(data)
            print(f"Sent {len(data)} bytes of data to: ('{server_name}',{server_port})")
            # s.sendto(data, (server_name, server_port))
            # echo = s.recv(64)

            # print(f"Received {len(echo)} bytes of echo\n")
            # print(echo)
            sleep(0.5)