#!/bin/sh

docker run --rm -it --name z15_python_server --net z15_network -e HOST="172.21.15.2" z15_2_5_python_server 8000

