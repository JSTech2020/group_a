import bert_serving.client as bert
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from pymongo import MongoClient

uri = 'mongodb://localhost:27017/'
database = 'zs_database'
collection_fetch = 'autotags'
collection_push = 'similarities'


df = pd.DataFrame()
db = object

client = MongoClient(uri)
db = client[database]

# retrieving only story id and details for now
df = pd.DataFrame(list(db[collection_fetch].find({}, {"_id":0, "lemmas": 1, "story_id": 1})))

client = bert.BertClient(check_length=False)

vectors = client.encode(df['lemmas'].values.tolist(), show_tokens=False, is_tokenized=True)

cos_sim = cosine_similarity(vectors)

# list of all story ids in order of retrieval
id_list = df['story_id'].values.tolist()

# check if push collection(autotags) already exists, if so, remove(drop) the collection for now
# TODO: handle exception
if collection_push in db.list_collection_names():
    collection = db[collection_push]
    if collection.estimated_document_count() != 0:
        print('Dropping the old collection (' + collection_push + ') ...')
        collection.drop()

collection = db[collection_push]

print("Top five similar story ids: ")

for i in range(0, len(id_list)):
    row = cos_sim[i]
    sort_five = np.argsort(-row)[:6]
    similar_story_ids = []
    for x in sort_five:
        # as each story would be completely similar to itself, we need to remove its id from the list
        if x != i:
            similar_story_ids.append(id_list[x])
    print("For story id - " + str(id_list[i]) + ":", end=" ")
    print(similar_story_ids)
    # insert related story_ids to database
    # TODO: exception handling
    collection.insert_one({
        "story_id": id_list[i],
        "related_story_id": similar_story_ids
    })

    # print(id_list[sort1[:6]])

