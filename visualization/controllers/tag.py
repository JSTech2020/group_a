from __main__ import app
from flask import jsonify

import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

URI = 'mongodb://localhost:27017/'
DATABASE = 'zs_database'
STORIES_DB = 'stories'
AUTOTAGS_DB = 'autotags'
SIMILARITIES_DB = 'similarities'

client = MongoClient(URI)
db = client[DATABASE]

@app.route('/tags', methods=['GET'])
def generate_tags():
    df = pd.DataFrame(list(db[AUTOTAGS_DB].find({}, {"_id":0, "story_id":1, "lemma_list_wo_verbs_and_names":1})))

    # extract key words for each story : Top 15
    corpus = []
    for i in range(len(df)):
        lemmas_l=[]
        persons=[]

        #entitie preprocessing:
        # We want to get rid of all the words which represents the name
        # for m in range(len(df['entities'][i])):
        #     if df['entities'][i][m][1]=='PER':
        #         persons.append(df['entities'][i][m][0])

        for j in range(len(df['lemma_list_wo_verbs_and_names'][i])):
    #         if df['pos'][i][j]!="PROPN" and (df['lemma_list_without_names_verbs'][i][j] not in persons) and df['lemma_list_without_names_verbs'][i][j]!="VERB":
              lemmas_l.append(df['lemma_list_wo_verbs_and_names'][i][j])
        corpus.append(' '.join(lemmas_l))

    result = keyword(corpus, 15)

    collection=db[SIMILARITIES_DB]
    for i in range(len(df)):
#         print(result[i])
        collection.update_one({"story_id": int(df['story_id'][i])},
                             {"$set": {"tags": result[i]}},
                             upsert=True)


    return jsonify({
                'status': 'success',
        })

"""
Using TF-IDF to extract key words from a cluster of text
"""
# input: list of string
# output: list of list of keywords
def keyword(corpus, topK):

    key_list = []

    # Word frequency matrix
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)

    # list of all words in Bag-of-Words model
    word = vectorizer.get_feature_names()

    # TF-IDF Matrix
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)

    # weight[i][j] represents the weight of word j in text i
    weight = tfidf.toarray()

    for i in range(len(weight)):
        keys=[]
        zipped = zip(word,weight[i])
        sorted_l=sorted(zipped,key=lambda t:t[1],reverse=True)

        for n in range(topK):
            keys.append(sorted_l[n][0])

        key_list.append(keys)

    return key_list

