from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

from app import app

mongo = PyMongo(app)

@app.route('/workOrder/create', methods=['POST'])
def add_workOrder():
    _json = request.json
    _name = _json['name']
    _description = _json['description']

    if _name and request.method == 'POST':
        id = mongo.db.workorders.insert({'name':_name, 'description':_description})
        # print()
        resp = jsonify("User added successfully")
        resp ={"_id":id, 'name':_name, 'description':_description} ,
        resp.status_code = 200
        return resp
    
    else:
        return not_found()

@app.route('/workOrders')
def workOrders():
    workOrders = mongo.db.workorders.find()
    resp = dumps(workOrders)
    return resp

@app.route('/workOrder/<id>')
def workOrder(id):
    workOrder = mongo.db.workorders.find_one({'_id':ObjectId(id)})
    resp = dumps(workOrder)
    return resp

@app.route('/workOrder/delete/<id>', methods=['DELETE'])
def workOrderDelete(id):
    mongo.db.workorders.delete_one({'_id':ObjectId(id)})
    resp = jsonify("The workOrder with Id " + id + " has been deleted")
    resp.status_code = 200
    return resp

@app.route('/workOrder/update/<id>', methods=['PUT'])
def workOrderUpdate(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _description = _json['description']
    if _name and _id and request.method == 'PUT':
        mongo.db.workorders.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name, 'description':_description}})
        resp = jsonify("User updated successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp




        


    
