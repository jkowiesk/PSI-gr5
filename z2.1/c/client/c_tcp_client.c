#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>

int work() { return 1; }
#define BUFSIZE 64
#define FIRST_BYTE_MASK 0xFF
int main() {
    int sfd, active_sfd;
    struct sockaddr_in servaddr, clientaddr;
    long temp_addr;
    char buf[BUFSIZE];
    int length;
    int bytes_read;

    sfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sfd < 0) {
        perror("Problem with creating a socket");
        exit(1);
    }
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = 0;
    //serwer otrzymuje port i IP przydzielony przez SO
    if (bind(sfd, (struct sockadrr *)&servaddr, sizeof(servaddr)) != 0) {
        perror("Problem with binding address");
        exit(1);
    }
    length = sizeof(servaddr);
    if (getsockname(sfd, (struct sockaddr *) &servaddr, &length) < 0) {
        perror("Problem with accessing received port");
        exit(1);
    }
    printf("Received port: %u\n", ntohs(servaddr.sin_port));
    //tryb pasywny gniazda
    if (listen(sfd, 32) != 0) {
        perror("Problem with calling listen");
        exit(1);
    }
    while (work()) {
        //odebranie połaczenia
        active_sfd = accept(sfd, &clientaddr, &length);
        if (active_sfd < 0) {
            perror("Problem with getting connection from client");
            exit(1);
        }
        //pętla czytania
        do {
            memset(buf, 0, sizeof(buf));
            if ((bytes_read = recv(active_sfd, buf, BUFSIZE-1, 0)) < 0) {
                perror("Problem with receiving data");
                exit(1);
            }
            printf("%s", buf);
            if (bytes_read == 0)
                printf("\n");
        } while (bytes_read > 0);
        if (close(active_sfd) != 0) {
            perror("Problem with closing active socket");
            exit(1);
        }

    }

    if (close(sfd) != 0) {
        perror("Problem with closing socket");
        exit(1);
    }

    return 0;
}