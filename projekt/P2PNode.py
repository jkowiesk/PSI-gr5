import socket
import threading
import time
from resourceHandler import ResourceHandler

UDP_PORT = 4000
TCP_PORT = 4001

class P2PNode:
    def __init__(self) -> None:
        self.res = {}
        self.connect()
        self.res_handler = ResourceHandler('./psi_projekt_download')


    def connect(self):
        self.broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_sock.bind(('', UDP_PORT))

        self.get_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.get_sock.bind(('', UDP_PORT + 1))

        self.file_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.file_sock.bind(('', TCP_PORT))

        self.stop = False

        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def listen(self):
        while not self.stop:
            data, addr = self.broadcast_sock.recvfrom(1024)
            message = data.decode()
            if message.startswith("FILES"):
                files = message[6:].split(",")
                self.files[addr] = files
                print(f'{addr} has files: {files}')
            if message.startswith("GET_NAMES"):
                filename = message[9:]
                if self.res_handler.check_resource(filename):
                    self.broadcast_sock.sendto("HAS_FILE".encode(), (addr[0], UDP_PORT + 1))
            elif message.startswith("GET_FILE"):
                filename = message[8:]
                if self.res_handler.files.get(filename, []) != []:
                    print("test")
                    self.file_sock.listen(5)
                    client, addr = self.file_sock.accept()
                    processed_file = self.res_handler.process_resource(filename)

                    for chunk in processed_file:
                        client.send(chunk)
                else:
                    self.udp_sock.sendto("FILE_NOT_FOUND".encode(), addr)
                self.file_sock.close()

    def share_files(self, filenames):
        self.files[("0.0.0.0", TCP_PORT)] = filenames
        message = "FILES" + ",".join(filenames)
        self.broadcast_sock.sendto(message.encode(), ('<broadcast>', TCP_PORT))

    def get_file(self, filename):
        message = "GET_NAMES" + filename
        self.broadcast_sock.sendto(message.encode(), ('<broadcast>', UDP_PORT))

        is_done = False
        while not is_done:
            _, peer = self.get_sock.recvfrom(1024)
            print(peer)
            is_done = True

        self.get_sock.sendto(f"GET_FILE{filename}".encode(), peer)

        is_connected = False
        while not is_connected:
            try:
                client, addr = self.file_sock.connect((peer[0], TCP_PORT + 1))
                is_connected = True
            except:
                continue

        with open(f"{self.res_handler.local_folder}/{filename}", 'wb') as f:
            data = b''
            while True:
                data = s.recv(1024)

                if not data:
                    break

                chunk = client.recv(1024)
                data += chunk.decode('utf-8')
                f.write(data)

    def stop(self):
        self.stop = True
        self.listen_thread.join()