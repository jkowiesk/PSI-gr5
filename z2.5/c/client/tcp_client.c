#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define ALPHABET "abcdefghijklmnopqrstuvwxyz"
#define MESSAGE_LENGTH 60
#define MESSAGE_NUMBER 10

struct arguments {
    struct hostent *host_address;
    u_int16_t port;
};

typedef struct arguments Arguments;

void get_random_string(char *buffer, size_t buffer_length) {
    size_t n;
    static char charset[] = ALPHABET;
    if (buffer_length) {
        if (buffer) {
            for (n = 0; n < buffer_length; ++n) {
                int key = rand() % (int)(sizeof(charset) - 1);
                buffer[n] = charset[key];
            }
        }
    }
}

void parse_arguments(int argc, char *argv[], Arguments *arguments) {
    char *host;
    u_int16_t port;
    struct hostent *host_info;

    if (argc < 3) {
        host = "localhost";
        port = htons(8000);
    } else {
        host = argv[1];
        if (port = atoi(argv[2]))
            port = htons(port);
        else {
            perror("Error, not able to parse provided arguments.");
            exit(1);
        }
    }

    host_info = gethostbyname(host);

    if (host_info == (struct hostent *)0) {
        fprintf(stderr, "%s: unknown host\n", host);
        exit(2);
    }

    printf("Will send to %s:%d\n", host, ntohs(port));

    arguments->host_address = host_info;
    arguments->port = port;
}
void sendMessage(char *buffer, size_t buffer_length, struct sockaddr_in *name) {
    int sock;
    ssize_t sent;
    size_t already_sent = 0;

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("opening datagram socket");
        exit(1);
    }

    if (connect(sock, (struct sockaddr *)name, sizeof(*name)) == -1) {
        perror("Connect");
        exit(3);
    }

    printf("Sending %s\n", buffer);

    while (already_sent < buffer_length) {
        sent = send(sock, buffer + already_sent, buffer_length - already_sent, 0);
        if (sent == -1) {
            perror("sending datagram message");
            exit(4);
        }
        already_sent += sent;
    }

    close(sock);
}

void sendMessageConcurrent(char *buffer, size_t buffer_length, struct sockaddr_in *name) {
    int pid = fork();
    if (pid == 0) {
        sendMessage(buffer, buffer_length, name);
        exit(0);
    } else if (pid == -1) {
        perror("Fork");
        exit(5);
    } else {
        printf("Forked process with pid %d\n", pid);
        fflush(stdout);
    }
}

int main(int argc, char *argv[]) {
    u_int8_t i;
    struct sockaddr_in name;
    Arguments arguments;
    char buffer[MESSAGE_LENGTH + 1];
    buffer[MESSAGE_LENGTH] = '\0';

    parse_arguments(argc, argv, &arguments);

    memcpy((char *)&name.sin_addr, (char *)arguments.host_address->h_addr, arguments.host_address->h_length);

    name.sin_family = AF_INET;
    name.sin_port = arguments.port;

    for (i = 0; i < MESSAGE_NUMBER; ++i) {
        get_random_string(buffer, MESSAGE_LENGTH);
        sendMessageConcurrent(buffer, MESSAGE_LENGTH, &name);
    }

    printf("Client finished.\n");
    fflush(stdout);

    return 0;
}