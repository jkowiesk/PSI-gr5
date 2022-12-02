#!/bin/sh

docker run --rm -it --name z15_python_client --net z15_network -e HOSTNAME="172.21.15.2" z15_z1_1_python_client 8000