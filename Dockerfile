FROM python:3.12-slim-bookworm

RUN apt update
RUN apt install -y git

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY *.py ./
COPY mqtt_bridge/*.py ./mqtt_bridge/

ENV DEVICES_CONFIG_LOCATION /etc/tapo-mqtt-bridge/devices.yml

ARG IMAGE_VERSION=Unknown
ENV IMAGE_VERSION=${IMAGE_VERSION}

CMD [ "python3", "-u", "main.py" ]
