setup:
	python3 -m venv ~./project2

install:
	sudo python3 -m pip install --upgrade pip &&\
	sudo python3 -m pip install -r requirements.txt &&\
	sudo python3 -m pip install --upgrade mplfinance &&\
	sudo apt-get install caca-utils
	
all:
	setup install
