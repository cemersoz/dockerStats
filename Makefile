all: build run

build:
	sudo docker build . -t ds-master
run:
	sudo docker run -d -v /veneristDS/contents:/veneristDS/contents ds-master

