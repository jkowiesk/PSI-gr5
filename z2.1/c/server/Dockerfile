FROM gcc:9.5

WORKDIR /src/

COPY . /src/

RUN gcc -o server c_tcp_server.c

ENTRYPOINT  ["./server"]
