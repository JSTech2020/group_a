from __main__ import app
from flask import jsonify

@app.route('/topic_model', methods=['GET'])
def generate_html():
    return jsonify({
        'status': 'success',
    })