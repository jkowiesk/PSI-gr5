import socket
import threading
from time import time
import os


class P2PNode:
    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port
        self.peers = set()
        self.res = {}
        self.change_download_folder('/psi_projekt_download')

    def change_download_folder(self, directory: str) -> None:
        self.download_dir = directory

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', self.port))
        self.stop = False
        self.broadcast_thread = threading.Thread(target=self.broadcast)
        self.broadcast_thread.start()
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def broadcast(self):
        while not self.stop:
            self.sock.sendto("SYS".encode(), (self.host, self.port))
            time.sleep(1)

    def listen(self):
        while not self.stop:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()
            if message.startswith("SYS"):
                self.peers.add(addr)
                self.sock.sendto("SYS/ACK".encode(), addr)
            elif message.startswith("SYS/ACK"):
                self.peers.add(addr)
            elif message.startswith("FILES"):
                files = message[6:].split(",")
                self.files[addr] = files
                print(f'{addr} has files: {files}')
            elif message.startswith("GET"):
                filename = message[4:]
                if filename in self.files.get(addr, []):
                    with open(filename, 'rb') as f:
                        bytes_to_send = f.read()
                        self.sock.sendto(bytes_to_send, addr)
                else:
                    self.sock.sendto("FILE_NOT_FOUND".encode(), addr)

    def share_files(self, filenames):
        self.files[("0.0.0.0", self.port)] = filenames
        message = "FILES" + ",".join(filenames)
        self.sock.sendto(message.encode(), (self.broadcast_address, self.port))

    def get_file(self, filename):
        for peer in self.peers:
            self.sock.sendto(f"GET{filename}".encode(), peer)
            data, _ = self.sock.recvfrom(1024)
            if data.decode() == "FILE_NOT_FOUND":
                continue
            with open(os.path.join(self.download_dir, filename), 'wb') as f:
                f.write(data)
                break
    
    def stop(self):
        self.stop = True
        self.listen_thread.join()
        self.broadcast_thread.join()