import socket
import sys

HOST = "127.0.0.1"
port = int(sys.argv[1])
MSG = "1234567890123456789012345"

def main():
    for i, func_name in enumerate(['send', 'sendall']):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("calling connect()")
            s.connect((HOST, port))
            print("after connect()\n")
            try:
                if i:
                    s.sendall(MSG.encode())
                else:
                    s.send(MSG.encode())
                print(f"Sent message using {func_name}: {MSG}")
            except OSError:
                print("Failed sending message")
            print(f"{func_name} ended")

if __name__ == "__main__":
    main()