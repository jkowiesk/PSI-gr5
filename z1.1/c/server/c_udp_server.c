#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define BUFFSIZE 5
#define ITERATIONS 3

void main(void) {
    int sock, length;
    struct sockaddr_in name;
    char buf[BUFFSIZE];
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("opening datagram socket");
        exit(1);
    }

    name.sin_family = AF_INET;
    name.sin_addr.s_addr = inet_addr("127.0.0.1");
    name.sin_port = htons(4001);;

    if (bind(sock,(struct sockaddr *)&name, sizeof name) == -1) {
        perror("binding datagram socket");
        exit(1);
    }

    length = sizeof(name);
    if (getsockname(sock,(struct sockaddr *) &name, &length) == -1) {
        perror("getting socket name");
        exit(1);
    }

    printf("Will listen on %s : %d\n", inet_ntoa(name.sin_addr), ntohs( name.sin_port));

    for (int i = 0; i < ITERATIONS; i++) {
        if ( read(sock, buf, BUFFSIZE) == -1 ) {
            perror("receiving datagram packet");
            exit(2);
            printf("-->%s\n", buf);
            close(sock);
            exit(0);
        } else
            printf("Message from Client: %s\n", buf);
    }
}