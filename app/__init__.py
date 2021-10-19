"""This is init module."""

from flask import Flask, json
from flask_pymongo import PyMongo
from config import *
import logging


# Place where app is defined
app = Flask(__name__)
app.config['MONGO_URI'] = DATABASE
logging.basicConfig(filename='record.log',level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


from app import api
#from app import task