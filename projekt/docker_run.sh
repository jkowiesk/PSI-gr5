docker build -t p2p-node .
docker run --rm -it --name node-one --network p2p-net p2p-node