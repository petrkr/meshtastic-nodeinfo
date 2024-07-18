FROM python:3.12-slim

RUN pip install --upgrade pip && \
    pip install meshtastic peewee

ADD info.py dbimport.py /app/
RUN chmod +x /app/info.py /app/dbimport.py

WORKDIR /app

ENTRYPOINT [ "/app/info.py" ]
