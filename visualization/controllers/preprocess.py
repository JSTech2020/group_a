from app import app
from flask import jsonify
from bson import json_util, ObjectId
import json

from pymongo import MongoClient

from utils_spacy import *

URI = 'mongodb://localhost:27017/'
DATABASE = 'zs_database'
STORIES_DB = 'stories'
AUTOTAGS_DB = 'autotags'
SIMILARITIES_DB = 'similarities'

client = MongoClient(URI)
db = client[DATABASE]

@app.route('/preprocess', methods=['GET'])
def preprocess():
    df = pd.DataFrame(list(db[STORIES_DB].find({}, {"_id":0, "id": 1, "plain_text": 1})))
    collection = db[AUTOTAGS_DB]

    for x in df.iterrows():
        # fetching id and content for each item in data-frame
        index, item = x
        story_id = item.id
        content = item.plain_text

        # clean text for each document
        content = removeUnwantedCharacters(content)

        # word tokenization and other preprocessing for each document
        token_list, lemma_list, pos_list, entity_list, noun_list, wo_verbs_and_names = tokenizeText(content)

        # insert if data is not present, else update
        collection.update_one(
            {"story_id": int(story_id)},
            {"$set":
                {
                    "story_id": story_id,
                    "tokens": token_list,
                    "lemmas": lemma_list,
                    "pos": pos_list,
                    "nouns": noun_list,
                    "entities": entity_list,
                    "lemma_list_wo_verbs_and_names": wo_verbs_and_names,
                    "preprocessed_text": content,
                }
            },
            upsert=True
        )

    return jsonify({
            'status': 'success',
    })