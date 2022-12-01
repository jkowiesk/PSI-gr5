FROM gcc:4.9

WORKDIR /src/

COPY . /src/

RUN gcc -o client udp_client.c

ENTRYPOINT  ["./client"]