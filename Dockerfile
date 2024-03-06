FROM python:3.12-alpine3.19

COPY requirements.txt /temp/requirements.txt
COPY upload /upload
WORKDIR /upload
EXPOSE 8000
