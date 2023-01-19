import socket
import threading
import time

class UDPFileSharer:
    def __init__(self, broadcast_address, port):
        self.broadcast_address = broadcast_address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("", self.port))
        self.peers = set()
        self.stop = False
        self.listen_thread = threading.Thread(target=self.listen)
        self.listen_thread.start()
        self.broadcast_thread = threading.Thread(target=self.broadcast)
        self.broadcast_thread.start()
        self.files = {}

    def listen(self):
        while not self.stop:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()
            if message.startswith("HELLO"):
                self.peers.add(addr)
                self.sock.sendto("HELLO_ACK".encode(), addr)
            elif message.startswith("HELLO_ACK"):
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

    def broadcast(self):
        while not self.stop:
            self.sock.sendto("HELLO".encode(), (self.broadcast_address, self.port))
            time.time.sleep(1)

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
            with open(filename, 'wb') as f:
                f.write(data)
                break
    def stop(self):
        self.stop = True
        self.listen_thread