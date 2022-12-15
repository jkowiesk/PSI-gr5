import socket
import string
from random import choices
from time import sleep

# Generate a random string of the specified size, using ASCII letters.
def generate_data(size):
    rand_str = ''.join(choices(string.ascii_letters, k=size))
    return str.encode(rand_str)

# The default size of the data to generate and send.
DATA_SIZE = 2

if __name__ == "__main__":
    # Parse the server name, port, and message from the command-line arguments.
    server_name = input("Enter the server's name: ")
    server_port = int(input("Enter the server's port: "))
    message = str.encode(input("Enter the message to send: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to the server.
        print("calling connect()")
        s.connect((server_name, server_port))
        print("after connect()\n")

        while True:
            # Generate and send the data.
            # data = generate_data(64)
            data = message
            s.send(data)
            print(f"Sent {len(data)} bytes of data to: ('{server_name}',{server_port})")

            # Wait before sending the next data.
            sleep(0.5)