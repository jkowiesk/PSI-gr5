FROM gcc:9.5

WORKDIR /src/

COPY . /src/

RUN gcc -o client c_tcp_client.c

CMD ["./client"]

