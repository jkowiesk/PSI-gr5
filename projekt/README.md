# Co robią dane metody

- init(self, host, port): This is the constructor for the P2PNode class. It initializes the instance variables host, port, peers, resources, and download_dir. host and port are the IP address and port number that the node will listen on for incoming connections. peers is a list of connections to other peers. resources is a dictionary that maps resource names to file paths for resources that are available on this node. download_dir is the directory where resources will be saved when they are downloaded.

- listen(self): This method starts a server that listens for incoming connections from other peers. It creates a socket, binds it to the specified IP address and port, and listens for incoming connections. For each incoming connection, it starts a new thread to handle the connection using the handle_peer() method.

- handle_peer(self, conn): This method handles incoming data from a peer connection. It receives data in 1024-byte chunks and decodes it into a string. If the data starts with the string "RESOURCES", it updates the list of resources for this peer using the update_resources() method. If the data starts with the string "REQUEST", it sends the requested resource to the peer using the send_resource() method

- update_resources(self, conn, resources): This method updates the list of resources for a given peer. It stores the list of resources in the resources dictionary, using the peer's connection conn as the key.

- send_resource(self, conn, resource): This method sends a requested resource to a peer. If the resource is available locally, it reads the file and sends the contents to the peer. If the resource is not available locally, it sends an error message to the peer.

- connect_to_peer(self, host, port): This method connects to another peer. It creates a socket, connects to the specified IP address and port, and adds the connection to the list of peers. It then starts a new thread to handle the connection using the handle_peer() method.

- broadcast_resources(self): This method broadcasts a list of available resources to all connected peers. It creates a message containing the list of resources, encoded as a string, and sends it to all of the peers in the peers list.

- request_resource(self, resource, peer): This method requests a specific resource from a peer. It sends a message to the peer containing the name of the resource.

- download_resource(self, resource, peer): This method downloads a resource from a peer. It first sends a request for the resource using the request_resource() method. It then receives the data for the resource in 1024-byte chunks and stores it in a variable. If the data starts with the string "ERROR", it prints the error message. Otherwise, it saves the data to a file in the download_dir directory and adds the resource to the list of available resources using the add_resource() method.

- add_resource(self, path): This method adds a new resource to the list of available resources. It extracts the resource name from the file path and stores it in the resources dictionary, using the resource name as the key and the file path as the value. It then broadcasts the updated list of resources to all connected peers using the broadcast_resources() method.

- list_resources(self): This method prints a list of available resources. It iterates through the keys in the resources dictionary and prints each resource name.
