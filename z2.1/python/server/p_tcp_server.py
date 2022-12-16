import socket
import sys
import os


# HOST = "127.0.0.1"
HOST = os.environ.get("HOST")
port = int(sys.argv[1])
bufferSize = 1024


def main():
    print("Will connect to ", HOST, ":", port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen(10)

        print(f"Listening on port {port} on {HOST} for incoming messages\n")

        while True:
            conn, address = s.accept()
            print(f"Connection successful.")

            with conn:
                print('Connect from: ', address)
                while True:
                    data = conn.recv(bufferSize)
                    data = data.decode("utf-8")
                    if not data:
                        break
                    print(f"Received: {data}\n")
                    conn.sendall(bytes(data, "utf-8"))
            conn.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()
