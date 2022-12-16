import socket
import sys
import threading

localIP = "127.0.0.1"
localPort = 8000
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
    host, port = get_host_and_port()
    print("Will connect to ", host, ":", port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(10)

        print(f"[LISTENING] Listening on port {port} on {host} for incoming messages\n")

        while True:
            conn, address = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def get_host_and_port():
    if len(sys.argv) < 3:
        print("no port and/or host, using localhost:8000")
        return localIP, localPort
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        return host, port


if __name__ == "__main__":
    main()