first: all

all:
	make -C Sources all
	make -C Documentation html

clean:
	make -C Sources clean
	make -C Documentation clean
