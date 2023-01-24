#!/bin/bash

docker build -t p2p-node .

mkdir res_two

docker run --rm -it --name node-two --network p2p-net -v $(pwd)/res_two:/app/res p2p-node python3 UI_not.py