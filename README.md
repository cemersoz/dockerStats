# DockerStats
This is the repository for a docker container that posts stats data to a provided endpoint. This container is designed to run on a remote device and publish device stats (currently only cpu and mem) to a remote server.

## The Docker Image
The docker image is built on top of a clean alpine implementation and is 33MB uncompressed. Other than standard alpine linux, it comes with python3, pip and the python package ```requests``` installed.

## The Python module
Every five seconds the main app reads data from the /proc directory and compiles a json object of cpu and memory stats. This is then posted to a server.

## Usage
To build the latest docker image run the command ```make build```. By default this builds the container specified in the Dockerfile with the name ```docker-stats```

To run a container with the image run the command ```make run```. By default this runs the latest ds-master image and mounts the /proc folder as /os_proc.

To build and run an image, you can just call ```make```
