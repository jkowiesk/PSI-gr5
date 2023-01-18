import socket

class Node:
    def __ini__(self):
        pass


    def listen_TCP(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', port))
        print(f'listening for TCP on {socket.gethostbyname(socket.gethostname())}:{port}')
        server_socket.listen()

        client_socket, client_address = server_socket.accept()

        client_socket.sendall(b'Hello, client!')

        client_socket.close()
        server_socket.close()

    
    def listen_broadcast(self, port):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.bind(('', port))
        print(f'listening for UDP on {socket.gethostbyname(socket.gethostname())}:{port}')
        while True:
            data, address = broadcast_socket.recvfrom(1024)
            print(f'Received broadcast from {address}: {data}')


    def message_TCP(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        data = client_socket.recv(1024)
        print('Received:', data)

        client_socket.close()


    def messasge_broadcast(self, port):
        broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_socket.sendto(b'Hello, peers!', ('<broadcast>', port))
        broadcast_socket.close()


def main():
    node = Node()

    while True:
        print('''
        1 - listen TCP
        2 - listen UDP
        3 - connect TCP to host
        4 - UDP broadcast a message
        * - quit
        ''')
        action = int(input('choose an action: '))
        if action == 1:
            port = int(input('port: '))
            node.listen_TCP(port)
        elif action == 2:
            port = int(input('port: '))
            node.listen_broadcast(port)
        elif action == 3:
            host = input('host: ')
            port = int(input('port: '))
            node.message_TCP(host, port)
        elif action == 4:
            port = int(input('port: '))
            node.messasge_broadcast(port)
        else:
            break


if __name__ == "__main__":
    main()
