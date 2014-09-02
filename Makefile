first: all

all:
	make -C source all
	make -C documentation html

clean:
	make -C source clean
	make -C documentation clean
