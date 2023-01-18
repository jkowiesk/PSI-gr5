# Working with Docker Networks

A quick guide for working with sockets inside docker networks

## Create a Docker Network

We need a docker network to put our containers in. We can create one with:

```
docker network create p2p-network
```

## Build the Image

Build the example image with the Node program:

```
docker build -t p2p-node .
```

## Create Nodes

Start off some nodes in our network:

```
docker run --rm -it --name node-one --network p2p-network p2p-node
```

```
docker run --rm -it --name node-two --network p2p-network p2p-node
```

```
docker run --rm -it --name node-three --network p2p-network p2p-node
```

> NOTE: Since we are using the -it flag, we need to start each of the containers in a new terminal

The nodes will be able to connect to each other now.
