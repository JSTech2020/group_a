from __main__ import app
# from flask import jsonify
from flask import render_template

@app.route('/topic_model', methods=['GET'])
def generate_html():
    return render_template('lda.html')
#     return jsonify({
#         'status': 'success',
#     })