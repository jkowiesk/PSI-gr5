FROM gcc:4.9

WORKDIR /src/

COPY . /src/

RUN gcc -o client c_udp_client.c

ENTRYPOINT  ["./client"]