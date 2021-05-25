FROM python:3.7-alpine
MAINTAINER Matías Cárdenas

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Creates a user that will be used for running applications only
RUN adduser -D user

# Switching docker to the user we just created
# This is for security purposes, otherwise Docker keeps running with the Root user with lots of privileges
USER user