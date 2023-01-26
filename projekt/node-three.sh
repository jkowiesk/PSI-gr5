#!/bin/bash

docker build -t p2p-node .

mkdir -m 777 res_three

docker run --rm -it --name node-three --network p2p-net -v $(pwd)/res_three:/app/res  -v $(pwd):/app p2p-node