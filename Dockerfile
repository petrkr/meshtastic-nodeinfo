FROM python:3.12-slim

RUN pip install --upgrade pip && \
    pip install meshtastic

ADD info.py /app/
RUN chmod +x /app/info.py

WORKDIR /app

ENTRYPOINT [ "/app/info.py" ]
