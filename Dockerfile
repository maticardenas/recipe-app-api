FROM python:3.7-alpine
MAINTAINER Matías Cárdenas

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# Create a folder to store all the media files
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# Creates a user that will be used for running applications only
#RUN adduser -D user

RUN adduser \
    --disabled-password \
    --gecos '' \
    --home /app \
user && chown -R user /app

# owner can do everything
RUN chown -R user:user /vol
# the rest can read and execute
RUN chown -R 755 /vol/web
# Switching docker to the user we just created
# This is for security purposes, otherwise Docker keeps running with the Root user with lots of privileges
USER user