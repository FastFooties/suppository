default:
	docker run --rm -it -v `pwd`:/data --workdir=/data adreeve/python-numpy python test.py

plot:
	docker run --rm -it -v `pwd`:/data --workdir=/data adreeve/python-numpy python test-plot.py

test-cgc:
	docker run --rm -it -v `pwd`:/data --workdir=/data adreeve/python-numpy python test-cgc.py
test-remainder:
	docker run --rm -it -v `pwd`:/data --workdir=/data adreeve/python-numpy python test-remainder.py
