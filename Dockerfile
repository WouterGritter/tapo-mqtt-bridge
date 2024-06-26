FROM python:3.12-slim-bookworm

RUN apt update
RUN apt install -y git

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY *.py ./
COPY mqtt_bridge/*.py ./mqtt_bridge/

CMD [ "python3", "-u", "main.py" ]
