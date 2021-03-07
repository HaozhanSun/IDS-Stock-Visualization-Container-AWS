FROM python:3.7.3-stretch

WORKDIR /app

COPY . stock.py /app/

RUN pip install --upgrade pip &&\
    pip install --trusted-host pypi.python.org -r requirements.txt &&\
    python3 -W ignore stock.py

    