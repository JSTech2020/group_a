from app import app


from flask import jsonify, request
from bson import json_util, ObjectId
import json
import tempfile

from pymongo import MongoClient
import pandas as pd
import csv

URI = 'mongodb://localhost:27017/'
DATABASE = 'zs_database'
STORIES_DB = 'stories'
AUTOTAGS_DB = 'autotags'
SIMILARITIES_DB = 'similarities'

client = MongoClient(URI)
db = client[DATABASE]

@app.route('/check_db', methods=['GET'])
def check_db():
    status=""
    errors=[]

    # check if stories table is present and populated
    if STORIES_DB not in db.list_collection_names():
        errors.append("Story data not found. Please populate the server using .csv file")

    if AUTOTAGS_DB not in db.list_collection_names():
        errors.append("Story metadata not found. Please run preprocessing. This functionality can be found in Nav bar link.")

    if SIMILARITIES_DB not in db.list_collection_names():
        errors.append("Story tags not found. Please generate tags. This functionality can be found in Nav bar link.")

    if len(errors)>0:
        status = "fail"
    else:
        status = "success"

    return jsonify({
                'status': status,
                'errors': errors
        })

@app.route('/upload_data', methods=['POST'])
def upload_data():
    # TODO Error handling
    status=""
    if request.method == 'POST':
        file = request.files['file']
        temp_path = tempfile.NamedTemporaryFile().name
        file.save(temp_path)
        df = pd.read_csv(temp_path,sep=';', engine='python')
        print(df)
#         df = df[(df['is_published'] == True)]
        data_dict = df.to_dict('records')
        collection = db[STORIES_DB]
        for row in data_dict:
            # filter to include only data with is_published is true
            if row["is_published"] == True:
                # insert if data is not present, else update
                collection.update_one(
                    {"story_id": int(row['id'])},
                    {"$set": row },
                    upsert=True
                )
        status = "success"
    else:
        status = "fail"

    return jsonify({
                    'status': status,

            })

