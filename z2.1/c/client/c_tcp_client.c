#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>

#define DEFAULT_PORT 8000
#define DEFAULT_SERVER_IP "127.0.0.1"

// Open a socket and connect to the specified server and port.
// Returns the socket identifier, or -1 if an error occurs.
int32_t open_socket(int32_t port, const char* server_ip) {
    int32_t socket_id = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_id < 0) {
        return -1;
    }

    struct sockaddr_in servaddr;
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(server_ip);
    servaddr.sin_port = htons(port);

    if (connect(socket_id, (struct sockaddr*) &servaddr, sizeof(servaddr))) {
        return -1;
    }

    return socket_id;
}

int main(int argc, char* argv[]) {
    static char const* message = "Message";

    // Parse the server IP and port from the command-line arguments,
    // or use the default values if none are provided.
    int32_t port = DEFAULT_PORT;
    const char* server_ip = DEFAULT_SERVER_IP;
    if (argc > 1) {
        server_ip = argv[1];
        if (argc > 2) {
            port = atoi(argv[2]);
        }
    }

    int32_t socket_id = open_socket(port, server_ip);
    if (socket_id < 0) {
        return -1;
    }

    if (write(socket_id, message, sizeof(message)) < 0) {
        return -1;
    }

    close(socket_id);
    return 0;
}
