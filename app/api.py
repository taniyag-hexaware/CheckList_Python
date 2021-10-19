from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request

from app import app

mongo = PyMongo(app)

#APIs for workOrder - GET,POST,DELETE,PUT

@app.route('/workOrder/create', methods=['POST'])
def add_workOrder():
    _json = request.json
    _name = _json['name']
    _description = _json['description']

    if _name and request.method == 'POST':
        id = mongo.db.workorders.insert({'name':_name, 'description':_description})
        # print()
        resp = jsonify("User added successfully")
        # resp ={"_id":id, 'name':_name, 'description':_description} ,
        resp.status_code = 200
        app.logger.info('WorkOrder sucessfully created!')
        return resp
    
    else:
        return not_found()

@app.route('/workOrders')
def workOrders():
    workOrders = mongo.db.workorders.find({},{'name':1})
    resp = dumps(workOrders)
    app.logger.info('WorkOrder sucessfully displayed!')
    return resp

@app.route('/workOrder/<id>')
def workOrder(id):
    workOrder = mongo.db.workorders.find_one({'_id':ObjectId(id)})
    resp = dumps(workOrder)
    app.logger.info('WorkOrder sucessfully displayed with id '+id)
    return resp

@app.route('/workOrder/delete/<id>', methods=['DELETE'])
def workOrderDelete(id):
    mongo.db.workorders.delete_one({'_id':ObjectId(id)})
    resp = jsonify("The workOrder with Id " + id + " has been deleted")
    resp.status_code = 200
    app.logger.info('WorkOrder sucessfully deleted wit id '+id)
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
        app.logger.info('WorkOrder sucessfully updated with id '+id)
        resp.status_code = 200
        return resp
    else:
        return not_found()



#APIs for task - GET,POST,DELETE,PUT


@app.route('/task/create', methods=['POST'])
def add_task():
    _json = request.json
    _task_name = _json['task_name']
    _task_description = _json['task_description']
    _wordOrderId = _json['wordOrderId']
    

    if _task_name and request.method == 'POST':
        id = mongo.db.tasks.insert({'task_name':_task_name, 'task_description':_task_description,'wordOrderId':ObjectId(_wordOrderId)})
        # print()
        resp = jsonify("Task added successfully")
        # resp ={"_id":id, 'task_name':_task_name, 'task_description':_task_description,'wordOrderId':ObjectId(_wordOrderId)} ,
        resp.status_code = 200
        app.logger.info('Task sucessfully created!')
        return resp
    
    else:
        return not_found()

@app.route('/tasks')
def tasks():
    tasks = mongo.db.tasks.find({},{'task_name':1})
    resp = dumps(tasks)
    app.logger.info('Task sucessfully displayed!')
    return resp

@app.route('/task/<id>')
def task(id):
    task = mongo.db.tasks.find_one({'_id':ObjectId(id)})
    resp = dumps(task)
    app.logger.info('Task sucessfully displayed with id '+id) 
    return resp

@app.route('/task/delete/<id>', methods=['DELETE'])
def taskDelete(id):
    mongo.db.tasks.delete_one({'_id':ObjectId(id)})
    resp = jsonify("The task with Id " + id + " has been deleted")
    resp.status_code = 200
    app.logger.info('task sucessfully deleted with id '+id) 
    return resp

@app.route('/task/update/<tid>', methods=['PUT'])
def taskUpdate(tid):
    _id = tid
    _json = request.json
    _name = _json['name']
    _description = _json['description']
    _wordOrderId = _json['wordOrderId']
    if _name and _id and request.method == 'PUT':
        mongo.db.tasks.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name, 'description':_description,'wordOrderId':ObjectId(_wordOrderId)}})
        resp = jsonify("task updated successfully")
        resp.status_code = 200
        app.logger.info('task successfully updated with id '+tid) 
        return resp
    else:
        return not_found()



#error handling

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found ' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    app.logger.error('404 page not found '+ request.url)
    return resp





        


    


        


    
