from __main__ import app
from flask import jsonify, request
from bson import json_util, ObjectId
import json


from pymongo import MongoClient

import pandas as pd
import numpy as np

from utils_nltk import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

URI = 'mongodb://localhost:27017/'
DATABASE = 'zs_database'
STORIES_DB = 'stories'
AUTOTAGS_DB = 'autotags'
SIMILARITIES_DB = 'similarities'

client = MongoClient(URI)
db = client[DATABASE]

@app.route('/similarities', methods=['GET'])
def similarities_all():
    similarities = db[SIMILARITIES_DB].find({},{"_id":0, "story_id":1, "related_story_id":1, "tags": 1})
    similarities = json.loads(json_util.dumps(similarities))
    return jsonify({
        'status': 'success',
        'similarities': similarities
    })

@app.route('/get_heatmap_data', methods=['GET'])
def compute_similarity():
    size = int(request.args.get('size')) if request.args.get('size') != None else 10
    df = pd.DataFrame(list(db[AUTOTAGS_DB].find({}, {"_id":0, "lemma_list_without_verbs":1,"lemmas":1, "preprocessed_text": 1, "story_id": 1})))

    stories = df['preprocessed_text'].head(size)
    num_story = len(stories)
    story_ids = ["story_" + str(i) for i in df['story_id']]
    id_list = list(df['story_id'])

    story_dict = dict(zip(story_ids, stories))
    ids = list(story_dict.keys())
    pairs = []
    for i, v in enumerate(ids):
        for j in ids[i+1:]:
	        pairs.append((ids[i], j))

    norm_story_corpus = stories

    vectorizer = TfidfVectorizer(min_df=0.0, max_df=1.0, ngram_range=(1, 1))
    feature_matrix = vectorizer.fit_transform(norm_story_corpus).astype(float)

    cos_sim = cosine_similarity(feature_matrix.toarray())


    result = []
    for i in range(0,len(cos_sim)):
        row=[]
        for j in range(0,i):
            row.append(cos_sim[i,j])
        result.append(row)

    pairwise_cosine_similarity = [compute_cosine_similarity(pair,cos_sim, id_list) for pair in pairs]
    df1 = pd.DataFrame({'pair': pairs, 'similarity': pairwise_cosine_similarity})

    df_hm = pd.DataFrame({'ind': range(num_story), 'cols': range(num_story), 'vals': pd.Series(np.zeros(num_story))})
    df_hm = df_hm.pivot(index='ind', columns='cols').fillna(0)
    df_temp = df1.copy()
    list1 = []
    list2 = []
    for item1, item2 in df_temp.pair:
        list1.append(item1)
        list2.append(item2)
    df_temp['l1'] = list1
    df_temp['l2'] = list2
    df_temp.drop('pair', axis=1, inplace=True)
    df_temp['l1'] = df_temp['l1'].apply(lambda x: int(x.split('_')[-1]))
    df_temp['l2'] = df_temp['l2'].apply(lambda x: int(x.split('_')[-1]))
    df_temp['pairs'] = list(zip(df_temp.l1, df_temp.l2, round(df_temp.similarity, 2)))
    for row, col, similarity in df_temp.pairs:
        df_hm.iloc[id_list.index(col), id_list.index(row)] = similarity

    df_most = df1.loc[[df1.similarity.values.argmax()]]
    df_least = df1.loc[[df1.similarity.values.argmin()]]


#     print(df2[0])
#
#     ms_id1, ms_id2 = df2[0]["pair"]
#     ls_id1, ls_id2 = df2[1]["pair"]
#
#     mostSimilar = {
#         "id1": ms_id1,
#         "id2": ms_id2,
#         "sim": df2[0]["similarity"]
#     }
#
#     leastSimilar = {
#         "id1": ls_id1,
#         "id2": ls_id2,
#         "sim": df2[1]["similarity"]
#     }

    # result =json.loads(json_util.dumps(df_hm.to_dict()))

#     group = []
#     variable = []
#     for i in range(0,len(pairwise_cosine_similarity)):
#         x,y = pairs[i]
#         group.append(x)
#         variable.append(y)
#
#     df3 = pd.DataFrame({'group': group, 'variable': variable, "value": pairwise_cosine_similarity})
#
#     return jsonify({
#         'status': 'success',
#         'ids': ids,
#         'result': df3.to_json(),
#         'mostSimilar': df_most.to_json(),
#         'leastSimilar': df_least.to_json()
#     })

    return jsonify({
            'status': 'success',
            'ids': ids,
            'result': result,
            'mostSimilar': df_most.to_json(),
            'leastSimilar': df_least.to_json()
    })

def compute_cosine_similarity(pair, cos_sim, id_list):
    text1, text2 = pair
    text1_index = id_list.index(int(text1.split("_")[1]))
    text2_index = id_list.index(int(text2.split("_")[1]))
    manual_cosine_similarity = cos_sim[text1_index][text2_index]
    return manual_cosine_similarity
