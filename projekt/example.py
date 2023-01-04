import socket
import threading
import os

class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.resources = {}
        self.download_dir = 'downloads'

    def listen(self):
        """Listen for incoming connections from other peers."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print(f'Listening for connections on {self.host}:{self.port}...')
        while True:
            conn, addr = s.accept()
            self.peers.append(conn)
            print(f'Connected to {addr}')
            # Start a new thread to handle the incoming connection
            thread = threading.Thread(target=self.handle_peer, args=(conn,))
            thread.start()

    def handle_peer(self, conn):
        """Handle incoming data from a peer connection."""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f'Received data from {conn.getpeername()}: {data}')
            message = data.decode()
            if message.startswith('RESOURCES'):
                # Update the list of resources for this peer
                resources = message[10:].split(',')
                self.update_resources(conn, resources)
            elif message.startswith('REQUEST'):
                # A peer is requesting a resource
                resource = message[8:]
                self.send_resource(conn, resource)
            else:
                # Echo the data back to the sender
                conn.sendall(data)
        conn.close()
        self.peers.remove(conn)
        print(f'Disconnected from {conn.getpeername()}')

    def update_resources(self, conn, resources):
        """Update the list of resources for a given peer."""
        self.resources[conn] = resources

    def send_resource(self, conn, resource):
        """Send a requested resource to a peer."""
        if resource in self.resources:
            # Check if the resource is available locally
            path = self.resources[resource]
            with open(path, 'rb') as f:
                conn.sendall(f.read())
        else:
            # Resource is not available locally, send an error message
            conn.sendall(b'ERROR: Resource not found')

    def connect_to_peer(self, host, port):
        """Connect to another peer."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        self.peers.append(s)
        print(f'Connected to {host}:{port}')
        # Start a new thread to handle the incoming connection
        thread = threading.Thread(target=self.handle_peer, args=(s,))
        thread.start()

    def broadcast_resources(self):
        """Broadcast a list of available resources to all connected peers."""
        message = 'RESOURCES ' + ','.join(self.resources.keys())
        message = message.encode()
        for peer in self.peers:
            peer.sendall(message)

    def request_resource(self, resource, peer):
        """Request a specific resource from a peer."""
        message = f'REQUEST {resource}'
        peer.sendall(message.encode())

    def download_resource(self, resource, peer):
        """Download a resource from a peer."""
        # Send the request for the resource
        self.request_resource(resource, peer)
        # Receive the data for the resource
        data = b''
        while True:
            chunk = peer.recv(1024)
            if not chunk:
                break
            data += chunk
        if data.startswith(b'ERROR'):
            print(data.decode())
        else:
            # Save the resource to the download directory
            path = os.path.join(self.download_dir, resource)
            with open(path, 'wb') as f:
                f.write(data)
            self.add_resource(path)
            print(f'Successfully downloaded {resource}')

    def add_resource(self, path):
        """Add a new resource to the list of available resources."""
        resource = os.path.basename(path)
        self.resources[resource] = path
        self.broadcast_resources()

    def list_resources(self):
        """Print a list of available resources."""
        print('Resources:')
        for resource in self.resources:
            print(resource)
        print('')