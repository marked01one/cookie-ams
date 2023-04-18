FROM ubuntu:latest
FROM python:3.10.6-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /web_project

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8000 5000

CMD ["bash", "-c", "./start.sh"] 