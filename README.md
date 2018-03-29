# dsMaster
This is the repository for the stats docker container. This container is designed to run on on each and every veneristDS device and publish os stats. 

## The Docker Image
The docker image is built on top of a clean alpine implementation and is 33MB uncompressed. Other than standard alpine linux, it comes with python3, pip and the python package ``requests``` installed.

## The Python module
Every five seconds the main app reads data from the /proc directory and compiles a json object of cpu and memory stats. This is then posted to the veneristDS server.

## Usage
To build the latest docker image run the command ```make build```. By default this builds the container specified in the Dockerfile with the name ```ds-stats```

To run a container with the image run the command ```make run```. By default this runs the latest ds-master image and mounts the /proc folder as /os_proc.

To build and run an image, you can just call ```make```
