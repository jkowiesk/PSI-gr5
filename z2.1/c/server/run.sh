#!/bin/sh

docker run --rm -it --name z15_c_server --net z15_network -e HOST="172.21.15.2" -e PORT="8000" z15_2_1_c_server
