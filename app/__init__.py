"""This is init module."""

from flask import Flask, json
from flask_pymongo import PyMongo
from werkzeug.utils import send_from_directory
from config import *
import logging
from flask_compress import Compress
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

# Place where app is defined
app = Flask(__name__)
Compress(app)
CORS(app)
app.config['MONGO_URI'] = DATABASE
logging.basicConfig(filename='record.log',level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')






from app import api
#from app import task


### swagger specific ###
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "CheckList_Python"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###