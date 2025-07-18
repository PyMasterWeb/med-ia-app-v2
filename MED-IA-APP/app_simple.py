import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS

app = Flask(__name__, static_folder=\'static\', static_url_path=\'\')
CORS(app)

@app.route(\'/\')
def index():
    return send_from_directory(app.static_folder, \'index.html\')

@app.route(\'/api/test\')
def api_test():
    return jsonify({\'status\': \'ok\', \'message\': \'API test endpoint working!\'})

