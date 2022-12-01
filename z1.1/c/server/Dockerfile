FROM gcc:4.9

WORKDIR /src/

COPY . /src/

RUN gcc -o server c_udp_server.c

ENTRYPOINT  ["./server"]
