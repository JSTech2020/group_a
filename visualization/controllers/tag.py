from __main__ import app
from flask import jsonify
import base64
from io import BytesIO

import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


from wordcloud import WordCloud, STOPWORDS
import re
from os import path
import string
from PIL import Image
import matplotlib.pyplot as plt



URI = 'mongodb://localhost:27017/'
DATABASE = 'zs_database'
STORIES_DB = 'stories'
AUTOTAGS_DB = 'autotags'
SIMILARITIES_DB = 'similarities'

client = MongoClient(URI)
db = client[DATABASE]

@app.route('/tags', methods=['GET'])
def generate_tags():
    df = pd.DataFrame(list(db[AUTOTAGS_DB].find({}, {"_id":0, "lemmas": 1, "story_id": 1, "tokens": 1, "pos": 1, "nouns":1, "entities":1, "preprocessed_text": 1})))
    corpus = get_corpus(df)

    collection=db["corpus"]
    collection.update_one({"id": 1},
                         {"$set": {"corpus": corpus}},
                         upsert=True)

    result = keyword(corpus, 5)

    #Adding similarities data when generating autotags
    cos_sim = find_similarity_matrix(df['preprocessed_text'])
    # list of all story ids in order of retrieval
    id_list = df['story_id'].values.tolist()

    collection=db[SIMILARITIES_DB]
    for i in range(len(df)):
        row = cos_sim[i]
        sort_five = np.argsort(-row)[:6]
        similar_story_ids = []
        for x in sort_five:
            # as each story would be completely similar to itself, we need to remove its id from the list
            if x!=i:
                similar_story_ids.append(id_list[x])
        # insert related story_ids and tags into database
        collection.update_one({"story_id": int(df['story_id'][i])},
                             {"$set": {"tags": result[i], "related_story_id" : similar_story_ids }},
                             upsert=True)

    return jsonify({
                'status': 'success',
        })

@app.route('/tags/word_cloud/<id>', methods=['GET'])
def generate_wordcloud(id):
    id = int(id)
    img_str = ""
    df = pd.DataFrame(list(db[AUTOTAGS_DB].find({}, {"_id":0, "lemmas": 1, "story_id": 1, "tokens": 1, "pos": 1, "nouns":1, "entities":1})))

    id_list = list(df['story_id'])

    # generate wordclod only if id is there in the database
    if id in id_list:
        #check if corpus is already in db else create new corpus
        if "corpus" in db.list_collection_names():
            df1 = pd.DataFrame(list(db['corpus'].find({}, {"_id":0, "corpus":1})))
            corpus = list(df1['corpus'][0])
        else:
            corpus = get_corpus(df)
            db['corpus'].update_one({"id": 1},
                      {"$set": {"corpus": corpus}},
                      upsert=True)

        #change the index number here to make different wordclouds
        index = id_list.index(id)

        d = path.dirname(__file__)
        alice_mask = np.array(Image.open(d+"/tree.png"))

        wordcloud = WordCloud(
            background_color='white',
            max_words=200,
            max_font_size=120,
            width=1000, height=800,
            random_state=42,
            mask=alice_mask
        ).generate(corpus[index]) #change the index number here to make different wordclouds

        img =  wordcloud.to_image()

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        status = "success"
        error = ""
    else:
        img_str = ""
        status = "fail"
        error = "Story not in database"


    return jsonify({
                    'status': status,
                    'imgStr': str(img_str),
                    'error': error
            })

def get_corpus(df):
    frequent_verbs=[]
    corpus = []
    most_freq, least_freq = frequency_count(df['lemmas'])
    for i in range(len(df)):
        lemmas_l=[]
        persons=[]

        #entitie preprocessing:
        # We want to get rid of all the words which represents the name
        for m in range(len(df['entities'][i])):
            if df['entities'][i][m][1]=='PER':
                persons.append(df['entities'][i][m][0])

        # Here we already remove the propn, entity names and verbs
        for j in range(len(df['lemmas'][i])):
            if df['pos'][i][j]!="PROPN" and (df['lemmas'][i][j] not in persons)and (df['lemmas'][i][j].lower() not in most_freq) and df['pos'][i][j]!="ADV":
                lemmas_l.append(df['lemmas'][i][j])
        corpus.append(' '.join(lemmas_l))
    return corpus


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

"""
Term_Frequency—Count
"""
def frequency_count(lemmas):
    word_count = {}
    for story in lemmas.values.tolist():
        for token in story:
            if token.lower() in word_count:
                word_count[token.lower()] +=1
            else:
                word_count[token.lower()] =1

    word_freq = []
    for word,freq in word_count.items():
        word_freq.append((word,freq))


    #sorted
    word_freq.sort(key = lambda x:x[1],reverse = True)
    num=len(word_freq)

    # generate the most and least frequent words
    most_freq=[]
    least_freq=[]
    for i in range(300):
        most_freq.append(word_freq[i][0])
        least_freq.append(word_freq[num-1-i][0])
    return most_freq, least_freq


# Find similarity matrix
def find_similarity_matrix(corpus):
    vectorizer = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1, 1))
    feature_matrix = vectorizer.fit_transform(corpus).astype(float)
    cos_sim = cosine_similarity(feature_matrix.toarray())
    return cos_sim
