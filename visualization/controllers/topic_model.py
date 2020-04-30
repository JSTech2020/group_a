from __main__ import app
# from flask import jsonify
from flask import render_template
# import required libraries
import sys
import re
import pandas as pd
import spacy
from pymongo import MongoClient

import gensim
import string
from gensim import corpora
from gensim.corpora.dictionary import Dictionary
from gensim.models.wrappers import LdaMallet
import os
import numpy as np
# Plotting tools
import pyLDAvis
import pyLDAvis.gensim  # don't skip this
import matplotlib.pyplot as plt
import json
import uuid 
from flask import request
import json

def topic_modeling_viz(num_topics=5):
    uri = 'mongodb://localhost:27017/'
    database = 'zs_database'
    collection_fetch = 'autotags_v2'
    collection_push = 'similarities'

    # initiate variables
    df = pd.DataFrame()
    db = object

    # connect to db. TODO: Handle exception cases
    client = MongoClient(uri)
    db = client[database]

    # retrieving required data
    df = pd.DataFrame(list(db[collection_fetch].find({}, {"_id":0, "lemma_list_without_verbs": 1, "story_id": 1})))

    final_doc = df["lemma_list_without_verbs"]
    dictionary = corpora.Dictionary(final_doc)
    DT_matrix = [dictionary.doc2bow(doc) for doc in final_doc]
    Lda_object = gensim.models.ldamodel.LdaModel
    lda_model_1 = Lda_object(DT_matrix, num_topics=num_topics, id2word = dictionary)
    #pyLDAvis.enable_notebook()
    vis = pyLDAvis.gensim.prepare(lda_model_1, DT_matrix, dictionary)
    file_path = f"./templates"
    file_name = f"/lda_{num_topics}_{uuid.uuid1()}.html"
    files = f"{file_path}/{file_name}"
    pyLDAvis.save_html(vis, files)
    return file_name
    
def topic_modeling_topic(num_topics,topic_id):
    uri = 'mongodb://localhost:27017/'
    database = 'zs_database'
    collection_fetch = 'autotags_v2'
    collection_push = 'similarities'

    # initiate variables
    df = pd.DataFrame()
    db = object

    # connect to db. TODO: Handle exception cases
    client = MongoClient(uri)
    db = client[database]

    # retrieving required data
    df = pd.DataFrame(list(db[collection_fetch].find({}, {"_id":0, "lemma_list_without_verbs": 1, "story_id": 1})))

    final_doc = df["lemma_list_without_verbs"]
    dictionary = corpora.Dictionary(final_doc)
    DT_matrix = [dictionary.doc2bow(doc) for doc in final_doc]
    Lda_object = gensim.models.ldamodel.LdaModel
    lda_model_1 = Lda_object(DT_matrix, num_topics=num_topics, id2word = dictionary)
    topics = lda_model_1.show_topic(topic_id)
    topics_list = []
    for i, (dicts, prob) in enumerate(topics):
        print(f"{i} {dicts} {prob}")
        print(type(prob))
        topic = {
       "word" : dicts,
       "prob": float(prob)
        }
        topics_list.append(topic)
    
    return topics_list 

@app.route('/topic_model', methods=['GET'])
def generate_html():
    args = request.args
    num_topics = args['num_topics']
    file_name=topic_modeling_viz(num_topics=num_topics)
    return render_template(file_name)
#     return jsonify({
#         'status': 'success',
#     })


@app.route('/topic_model_viz', methods=['GET'])
def generate_json():
    args = request.args
    num_topics = args['num_topics']
    topic_id = args['topic_id']
    topics= topic_modeling_topic(num_topics=int(num_topics),topic_id=int(topic_id))
        
    return json.dumps(topics)
