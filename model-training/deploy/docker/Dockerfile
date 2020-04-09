############
### BASE ###
############
FROM python:3.7 as base

RUN apt-get install wget

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN python -m spacy download de_core_news_sm

COPY source /source
COPY models /models
COPY examples /examples

WORKDIR /models
RUN bert-serving-start -model_dir ./multi_cased_L-12_H-768_A-12/ -num_worker=1 -show_tokens_to_client

WORKDIR /
WORKDIR /examples
RUN jupyter notebook





