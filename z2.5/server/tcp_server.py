import socket
import sys
import threading
import os

<<<<<<< HEAD:z2.5/server/tcp_server.py
HOST = "127.0.0.1"
port = int(sys.argv[1])

=======

localIP = os.environ.get("HOST")
localPort = 8000
>>>>>>> 0bb54f2ae0aa539e6c13eb5d5514b30192981254:z2.5/python/server/tcp_server.py
bufferSize = 1024


def handle_client(conn, address):
    print(f"[NEW CONNECTION] {address} connected")
    with conn:
        message = ''
        while True:
            data = conn.recv(bufferSize)
            if not data:
                break
            print(f"[MESSAGE] Received: {data}\n")
            message += data.decode("utf-8")
            conn.sendall(bytes(message, "utf-8"))
    conn.close()
    print(f"[CLOSING] Connection with {address} closed.")


def main():
    print("Will connect to ", HOST, ":", port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen(10)

        print(f"[LISTENING] Listening on port {port} on {HOST} for incoming messages\n")

        while True:
            conn, address = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()

