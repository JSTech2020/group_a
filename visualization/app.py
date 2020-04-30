from flask import Flask, jsonify
from flask_cors import CORS
from bson import json_util, ObjectId
import json





# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)

# enable CORS
#CORS(app, resources={r'/*': {'origins': '*'}})
CORS(app)


import controllers.story
import controllers.preprocess
import controllers.tag
import controllers.similarity
import controllers.topic_model


if __name__ == '__main__':
    app.run()