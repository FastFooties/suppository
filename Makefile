default:
	docker run --rm -it -v `pwd`:/data --workdir=/data adreeve/python-numpy python test.py

plot:
	docker run --rm -it -v `pwd`:/data --workdir=/data adreeve/python-numpy python test-plot.py
