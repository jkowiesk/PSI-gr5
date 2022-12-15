import socket
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8001
MESSAGE = "ABCDEFGHIJKLMOPQRSTUVWXYZ"

def main():
    host_addr = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_HOST
    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT
    for idx, func_name in enumerate(['send', 'sendall']):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host_addr, port))
                print(f"Connected to {host_addr}:{port}")
            except OSError:
                print("Failed connection to server")
            try:
                if idx:
                    s.sendall(MESSAGE.encode())
                else:
                    s.send(MESSAGE.encode())
                print(f"Sent message using {func_name}: {MESSAGE}")
            except OSError:
                print("Failed sending message")
if __name__ == "__main__":
    main()