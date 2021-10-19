"""This is init module."""

from flask import Flask, json
from flask_pymongo import PyMongo
from config import *


# Place where app is defined
app = Flask(__name__)
app.config['MONGO_URI'] = DATABASE

from app import workOrder
#from app import task