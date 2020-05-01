from __main__ import app
# from flask import jsonify
from flask import render_template,jsonify
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

uri = 'mongodb://localhost:27017/'
database = 'zs_database'
collection_fetch = 'autotags_v2'
collection_push = 'similarities'
collection_stories = 'stories'
lda_model_dict = {}
lda_viz_dict = {}

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
texts = pd.DataFrame(list(db[collection_stories].find({}, {"_id":0, "title": 1, "id": 1, "abstract": 1})))


def get_lda_model(num_topics):
    if lda_model_dict.get(num_topics): 
         return lda_model_dict.get(num_topics)
    else:
        Lda_object = gensim.models.ldamodel.LdaModel
        lda_model_1 = Lda_object(DT_matrix, num_topics=num_topics, id2word = dictionary)
        lda_model_dict[num_topics] = lda_model_1
        return lda_model_1
        

def topic_modeling_viz(num_topics=5):
    file_name = f"/lda_{num_topics}_{uuid.uuid1()}.html"
    if lda_viz_dict.get(file_name):
        return lda_viz_dict.get(file_name)
    else:
        lda_model_1 = get_lda_model(num_topics)
        #pyLDAvis.enable_notebook()
        vis = pyLDAvis.gensim.prepare(lda_model_1, DT_matrix, dictionary)
        file_path = f"./templates"
        files = f"{file_path}/{file_name}"
        pyLDAvis.save_html(vis, files)
        lda_viz_dict[file_name] = file_name
        return file_name
    
def topic_modeling_topic(num_topics,topic_id):
    lda_model_1 = get_lda_model(num_topics)
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

def get_stories_for_topic_id(num_topics,topic_id):
    ldamodel= get_lda_model(num_topics)
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[DT_matrix]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic, Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    sent_topics_df = pd.concat([sent_topics_df, texts], axis=1)
    df_dominant_topic = sent_topics_df.reset_index()
    df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords','Story_Id','Title','Abstract']

    return(df_dominant_topic[df_dominant_topic['Dominant_Topic'] == topic_id].to_json(orient='records'))


@app.route('/topic_model', methods=['GET'])
def generate_html():
    args = request.args
    num_topics = args['num_topics']
    file_name=topic_modeling_viz(num_topics=num_topics)
    return render_template(file_name)
#     return jsonify({
#         'status': 'success',
#     })


@app.route('/topic_model_word_cloud', methods=['GET'])
def generate_word_clound():
    args = request.args
    num_topics = args['num_topics']
    topic_id = args['topic_id']
    topics= topic_modeling_topic(num_topics=int(num_topics),topic_id=int(topic_id))
    return jsonify({
            'topics': topics,
    })
    #return json.dumps(topics)



@app.route('/topic_model_stories', methods=['GET'])
def generate_topic_stories():
    args = request.args
    num_topics = args['num_topics']
    topic_id = args['topic_id']
    topics= get_stories_for_topic_id(num_topics=int(num_topics),topic_id=int(topic_id))
        
    return jsonify({
            'topics': topics,
    })
