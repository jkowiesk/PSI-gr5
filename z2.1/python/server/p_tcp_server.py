import socket
import sys

localIP = "127.0.0.1"
localPort = 8000
bufferSize = 1024


def main():
    host, port = get_host_and_port()
    print("Will connect to ", host, ":", port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(10)

        print(f"Listening on port {port} on {host} for incoming messages\n")

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