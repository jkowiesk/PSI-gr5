#!/bin/bash

docker build -t p2p-node .

mkdir res_one

docker run --rm -it --name node-one --network p2p-net -v $(pwd)/res_one:/app/res  -v $(pwd):/app p2p-node
