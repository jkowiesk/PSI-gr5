#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define h_addr h_addr_list[0]


const char* HOST = "127.0.0.1";
const char* DATA = "test";

int main(int argc, char *argv[]) {
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
    printf(" : %i", htons( atoi( argv[2] )));

    if (sendto(sock, DATA, sizeof DATA ,0, (struct sockaddr *) &name,sizeof name) == -1) {
        perror("sending datagram message");
        close(sock);
        exit(0);
    }
}
