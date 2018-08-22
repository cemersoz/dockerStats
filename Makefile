all: build run

build:
	sudo docker build . -t ds-stats
run:
	sudo docker run -d -v /proc:/host-proc ds-stats

