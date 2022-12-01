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

int main(int argc, char *argv[]) {
    char* data[3] = {"test1", "test2", "test3"};


    int sock;
    struct sockaddr_in name;
    struct hostent *hp;

    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock == -1) {
        perror("opening datagram socket");
        exit(1);
    }

    hp = gethostbyname(argv[1]);
    printf("Host %s", hp->h_name);

    if (hp == (struct hostent *) 0) {
        fprintf(stderr, "%s: unknown host\n", argv[1]);
        exit(2);
    }
    memcpy((char *) &name.sin_addr, (char *) hp->h_addr, hp->h_length);
    name.sin_family = AF_INET;
    name.sin_port = htons( atoi( argv[2] ));
    printf(" : %i\n", atoi( argv[2] ));


    for (int i = 0; i < 3; i++) {
        if (sendto(sock, (const char *) data[i], BUFFSIZE, 0, (struct sockaddr *) &name,sizeof name) == -1) {
            perror("sending datagram message");
            close(sock);
            exit(0);
        } else {
            printf("Sent #%d datagram\n", i+1);
        }
    }
}
