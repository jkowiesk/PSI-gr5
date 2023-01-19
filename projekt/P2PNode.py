import socket
import threading
from time import time
import os
from resourceHandler import ResourceHandler


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
                    processed_file, packets_amount = ResourceHandler().process_resource(filename)
                    self.sock.sendto(packets_amount, addr)
                    for chunk in processed_file:
                        self.sock.sendto(chunk, addr)
                else:
                    self.sock.sendto("FILE_NOT_FOUND".encode(), addr)

    def share_files(self, filenames):
        self.files[("0.0.0.0", self.port)] = filenames
        message = "FILES" + ",".join(filenames)
        self.sock.sendto(message.encode(), (self.broadcast_address, self.port))

    def get_file(self, filename):
        for peer in self.peers:
            self.sock.sendto(f"GET{filename}".encode(), peer)
            packet_amount, _ = self.sock.recvfrom(1024) 
            
            if packet_amount.decode() == "FILE_NOT_FOUND":
                continue

            with open(os.path.join(self.download_dir, filename), 'wb') as f:
                data = b''
                for _ in range(packet_amount):
                    chunk, _ = self.sock.recvfrom(1024)
                    data += chunk.decode('utf-8')
                f.write(data)
                break
    
    def stop(self):
        self.stop = True
        self.listen_thread.join()
        self.broadcast_thread.join()