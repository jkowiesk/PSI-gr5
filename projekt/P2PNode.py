import socket
import threading
import time
import os
from resourceHandler import ResourceHandler

UDP_PORT = 4000
TCP_PORT = 4001

class P2PNode:
    def __init__(self) -> None:
        self.peers = set()
        self.res = {}
        self.connect()
        self.res_handler = ResourceHandler('./psi_projekt_download')

    def connect(self):
        self.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_sock.bind(('', UDP_PORT))
        self.stop = False

        self.broadcast_thread = threading.Thread(target=self.broadcast)
        self.broadcast_thread.start()
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()

    def broadcast(self):
        while not self.stop:
            self.udp_sock.sendto("SYS".encode(), ('<broadcast>', UDP_PORT))
            time.sleep(1)

    def listen(self):
        while not self.stop:
            data, addr = self.udp_sock.recvfrom(1024)
            message = data.decode()
            if message.startswith("SYS"):
                self.peers.add(addr)
                self.udp_sock.sendto("SYS/ACK".encode(), addr)
            elif message.startswith("SYS/ACK"):
                self.peers.add(addr)
            elif message.startswith("FILES"):
                files = message[6:].split(",")
                self.files[addr] = files
                print(f'{addr} has files: {files}')
            elif message.startswith("GET"):
                filename = message[3:]
                if self.res_handler.files.get(filename, []) != []:
                    print("test")
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.bind(("", TCP_PORT + 1))
                    s.listen(5)
                    client, addr = s.accept()
                    processed_file, packets_amount = self.res_handler.process_resource(filename)

                    client.send(packets_amount)      # tu się wywala, chyba trzeba jakoś zamienic na bajty
                    for chunk in processed_file:
                        client.send(chunk)
                else:
                    self.udp_sock.sendto("FILE_NOT_FOUND".encode(), addr)

    def share_files(self, filenames):
        self.files[("0.0.0.0", UDP_PORT)] = filenames
        message = "FILES" + ",".join(filenames)
        self.udp_sock.sendto(message.encode(), (self.broadcast_address, self.port))

    def get_file(self, filename):
        # print(self.peers)
        for peer in self.peers:
            print(peer)
            self.udp_sock.sendto(f"GET{filename}".encode(), peer)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("", TCP_PORT))
            time.sleep(0.1)       # to jest żeby listen zdążył zrobić .accept()
            client, addr = s.connect((peer[0], TCP_PORT + 1))
            packet_amount = client.recv(1024)
            print(packet_amount)
            with open(f"{self.res_handler.local_folder}/{filename}", 'wb') as f:
                data = b''
                for _ in range(int(packet_amount.decode())):
                    chunk = client.recv(1024)
                    data += chunk.decode('utf-8')
                f.write(data)
                break

    def stop(self):
        self.stop = True
        self.listen_thread.join()
        self.broadcast_thread.join()