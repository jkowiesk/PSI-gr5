import socket
import threading
import os
import time
from resourceHandler import ResourceHandler

PORT = 4000
BATCH_SIZE = 1024

END_CONNECTION = b'\x00'

class P2PNot:
    def __init__(self) -> None:
        self.res_handler = ResourceHandler(os.getenv('RESOURCES_DIR'))
        self.resources = set(self.res_handler.scan_local_folder().keys())
        self.connect()

    def connect(self):
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_sock.bind(('', PORT))

        self.get_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_sock.bind(('', PORT + 1))

        self.stop = False

        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

        self.share_files()

    def listen(self):
        while not self.stop:
            data, addr = self.broadcast_sock.recvfrom(BATCH_SIZE)

            if data == END_CONNECTION:
                return

            if socket.gethostbyname(socket.gethostname()) == addr[0]:
                continue

            message = data.decode()
            if message.startswith("FILES"):
                files = message[5:].split(",")
                self.resources.update(files)
            if message.startswith("GET_NAME"):
                filename = message[8:]
                if self.res_handler.check_resource(filename):
                    self.broadcast_sock.sendto("HAS_FILE".encode(), (addr[0], PORT + 1))
            elif message.startswith("GET_FILE"):
                filename = message[8:]

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
                    s.bind(("", PORT))
                    s.listen(1)
                    client, addr = s.accept()

                    client.close()

    def share_files(self):
        message = "FILES" + ",".join(self.resources)
        self.broadcast_sock.sendto(message.encode(), ('<broadcast>', PORT))

    def get_file(self, filename):
        message = "GET_NAME" + filename
        self.broadcast_sock.sendto(message.encode(), ('<broadcast>', PORT))

        is_done = False
        while not is_done:
            _, peer = self.get_sock.recvfrom(BATCH_SIZE)
            is_done = True

        self.get_sock.sendto(f"GET_FILE{filename}".encode(), peer)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", PORT + 1))
            while not is_connected:
                try:
                    print(peer)
                    s.connect((peer[0], PORT))
                    is_connected = True
                except:
                    continue

            with open(f"{self.res_handler.local_folder}/{filename}", 'wb') as f:
                while True:
                    data = s.recv(BATCH_SIZE)
                    print(data)

                    if data == END_CONNECTION or END_CONNECTION in data:
                        break

                    if data == b"":
                        raise socket.error

                    f.write(data)

    def stop_node(self):
        self.broadcast_sock.sendto(END_CONNECTION, ("127.0.0.1", PORT))
        self.listen_thread.join()