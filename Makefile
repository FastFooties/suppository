default: run

build: Dockerfile
	docker build -t mathijs-gcgcd .

run: build
	docker run --rm -it -v `pwd`:/data --workdir=/data mathijs-gcgcd python test.py
