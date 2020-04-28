from __main__ import app
from flask import jsonify
import json
from bson import json_util, ObjectId
from pymongo import MongoClient

URI = 'mongodb://localhost:27017/'
DATABASE = 'zs_database'
STORIES_DB = 'stories'
AUTOTAGS_DB = 'autotags'

client = MongoClient(URI)
db = client[DATABASE]

#retrieve all stories
@app.route('/stories', methods=['GET'])
def all_stories():
    stories = db[STORIES_DB].find({},{"_id":0, "id":1, "title":1})
    stories = json.loads(json_util.dumps(stories))
    return jsonify({
        'status': 'success',
        'stories': stories
    })

@app.route('/stories/<id>', methods=['GET'])
def one_story(id):
    #story = list(db[STORIES_DB].find({"id": int(id)}, {"_id":0, "id":1, "title":1, "abstract":1}))
    story = list(db[STORIES_DB].find({"id": int(id)}, {"_id":0, "id":1, "title":1, "abstract":1,"content":1, "plain_text": 1}))
    story = json.loads(json_util.dumps(story))
    return jsonify({
	'story': story,
        'status': 'success'
    })