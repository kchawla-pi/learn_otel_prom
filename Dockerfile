FROM python:3.11
LABEL authors="kc547"

WORKDIR /simple_server
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY main.py ./
