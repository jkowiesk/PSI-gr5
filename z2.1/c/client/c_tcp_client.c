#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>

#define DEFAULT_PORT 8888
#define DEFAULT_SERV_IP "127.0.0.1"

int main(int argc, char* argv[]) {
    static char const* message = "PSI test message for second exercise";

    int32_t port = DEFAULT_PORT;
    const char* server_ip = DEFAULT_SERV_IP;
    if (argc > 1) {
        server_ip = argv[1];
        if (argc > 2) {
            port = atoi(argv[2]);
        }
    }

    int32_t socket_id = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_id < 0) {
        return -1;
    }

    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr(server_ip);
    serv_addr.sin_port = htons(port);

    if (connect(socket_id, (struct sockaddr*) &serv_addr, sizeof(serv_addr))) {
        return -1;
    }

    if (write(socket_id, message, sizeof(message)) < 0) {
        return -1;
    }

    close(socket_id);
    return 0;
}
