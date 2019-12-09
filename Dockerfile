FROM python:3.7.5-buster

RUN mkdir -p /opt/avena-socketServer

COPY ./socketServer/. /opt/avena-socketServer/

RUN cd /opt/avena-socketServer ; pip install -r requirements.txt
CMD cd /opt/avena-socketServer ; python3 server.py

EXPOSE 5000

