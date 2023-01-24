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
        self.res = {}
        self.res_handler = ResourceHandler(os.getenv('RESOURCES_DIR'))
        self.resources = set(self.res_handler.scan_local_folder().keys())
        self.connect()

    def connect(self):
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_sock.bind(('', PORT))

        self.get_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_sock.bind(('', PORT + 1))

        self.file_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.file_sock.bind(('', PORT))

        self.stop = False

        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

        self.share_files()

    def listen(self):
        while not self.stop:
            data, addr = self.broadcast_sock.recvfrom(1024)

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
                self.file_sock.listen(5)
                print("XD")
                client, addr = self.file_sock.accept()

                client.close()
                self.file_sock.shutdown(socket.SHUT_RD)

    def share_files(self):
        message = "FILES" + ",".join(self.resources)
        self.broadcast_sock.sendto(message.encode(), ('<broadcast>', PORT))

    def get_file(self, filename):
        message = "GET_NAME" + filename
        self.broadcast_sock.sendto(message.encode(), ('<broadcast>', PORT))

        is_done = False
        while not is_done:
            _, peer = self.get_sock.recvfrom(1024)
            is_done = True

        self.get_sock.sendto(f"GET_FILE{filename}".encode(), peer)

        is_connected = False
        while not is_connected:
            try:
                self.file_sock.connect((peer[0], PORT))
                is_connected = True
            except:
                continue

        with open(f"{self.res_handler.local_folder}/{filename}", 'wb') as f:
            while True:
                data = self.file_sock.recv(1024)

                if data == END_CONNECTION:
                    break

                if data == "":
                    raise socket.error

                f.write(data)
        return 0

    def stop_node(self):
        self.broadcast_sock.sendto(END_CONNECTION, ("127.0.0.1", PORT))
        self.listen_thread.join()