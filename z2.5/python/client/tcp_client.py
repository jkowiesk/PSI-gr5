import socket
import string
import sys
import os
from random import choices
from time import sleep


HOST = os.environ.get("HOST")
port = int(sys.argv[1])

DATA_SIZE = 512

# Generate a random string of the specified size, using ASCII letters.
def generate_data(size):
    rand_str = ''.join(choices(string.ascii_letters, k=size))
    return str.encode(rand_str)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server.
        print("calling connect()")
        s.connect((HOST, port))
        print("after connect()\n")
        data = generate_data(DATA_SIZE)
        s.send(data)
        s.close()

if __name__ == "__main__":
    main()

