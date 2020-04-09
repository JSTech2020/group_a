############
### BASE ###
############
FROM python:3.7 as base

RUN apt-get install wget

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY source /source

WORKDIR /
