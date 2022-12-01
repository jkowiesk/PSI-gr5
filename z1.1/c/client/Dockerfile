FROM gcc:4.9

WORKDIR /src/

COPY . /src/

RUN gcc -o client -std=c11 c_udp_client.c

ENTRYPOINT  ["./client"]