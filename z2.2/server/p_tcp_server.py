import socket
import sys
import os


HOST = os.environ.get("HOST")
port = int(sys.argv[1])
bufferSize = 8

def main():
    print("Will connect to ", HOST, ":", port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, port))
        s.listen(10)

        print(f"Listening on port {port} on {HOST} for incoming messages\n")

        while True:
            conn, addr = s.accept()
            with conn:
                i = 1
                print('Connect from: ', addr)
                message = ""
                while True:
                    data = conn.recv(bufferSize)
                    print("\n", str(data, 'utf-8'))
                    if not data:
                        break
                    print('sending buffer #', i)
                    message += data.decode()
                    i += 1
                conn.send(b'This is answer from server')
            print("Full message: ", message)
            print("Connection closed by client")

if __name__ == "__main__":
    main()
