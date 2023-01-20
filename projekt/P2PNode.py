import socket
import threading
import os

from resourceHandler import ResourceHandler

PORT = 4000
BATCH_SIZE = 1024

END_CONNECTION = b'\x00'

class P2PNode:
    def __init__(self) -> None:
        self.res = {}
        self.connect()
        self.res_handler = ResourceHandler(os.getenv('RESOURCES_DIR'))


    def connect(self):
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_sock.bind(('', PORT))

        self.get_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_sock.bind(('', PORT + 1))

        self.file_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_sock.bind(('', PORT))

        self.stop = False

        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def listen(self):
        while not self.stop:
            data, addr = self.broadcast_sock.recvfrom(1024)

            if socket.gethostbyname(socket.gethostname()) == addr[0]:
                continue
            message = data.decode()
            if message.startswith("FILES"):
                files = message[6:].split(",")
                self.files[addr] = files
                print(f'{addr} has files: {files}')
            if message.startswith("GET_NAMES"):
                filename = message[9:]
                if self.res_handler.check_resource(filename):
                    self.broadcast_sock.sendto("HAS_FILE".encode(), (addr[0], PORT + 1))
            elif message.startswith("GET_FILE"):
                filename = message[8:]
                self.file_sock.listen(5)
                client, addr = self.file_sock.accept()

                processed_file = self.res_handler.process_resource(filename)

                for chunk in self.res_handler.divide_into_batches(processed_file, BATCH_SIZE):
                    client.send(chunk)
                else:
                    client.send("FILE_NOT_FOUND".encode())
                client.send(END_CONNECTION)
                client.close()

    def share_files(self, filenames):
        self.files[("0.0.0.0", PORT)] = filenames
        message = "FILES" + ",".join(filenames)
        self.broadcast_sock.sendto(message.encode(), ('<broadcast>', PORT))

    def get_file(self, filename):
        message = "GET_NAMES" + filename
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

                f.write(data)

    def stop_node(self):
        self.stop = True
        self.listen_thread.join()