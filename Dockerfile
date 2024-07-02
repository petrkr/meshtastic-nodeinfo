FROM python:3.12-slim

RUN pip install --upgrade pip && \
    pip install meshtastic

ADD info.py /app/

WORKDIR /app

CMD ["python", "info.py"]
