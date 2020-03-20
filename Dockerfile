FROM python:3.6-slim

WORKDIR /home/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /home/app

ENTRYPOINT python -u /home/app/run.py
