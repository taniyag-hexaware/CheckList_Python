from typing import Optional
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from pydantic import BaseModel
from flask_pydantic import validate
from pydantic.types import constr
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import send_from_directory


from app import app


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    # config={
    #     'app_name': "CheckList_Python"
    # }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

mongo = PyMongo(app)

class WorkOrder(BaseModel):
    name:str
    description:str

class Task(BaseModel):
    task_name:str
    task_description:str
    wordOrderId:str 

 

#Swagger

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static',path)


#APIs for workOrder - GET,POST,DELETE,PUT
@app.route('/')
def homePage():
    return "Welcome To checkpyth"

@app.route('/workOrder/create', methods=['POST'])
@validate()
def add_workOrder(body : WorkOrder):
    _json = request.json
    _name = body.name
    _description = body.description

    if _name and request.method == 'POST':
        id = mongo.db.workorders.insert({'name':_name, 'description':_description})
        #print(id)
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
@validate()
def workOrder(id:str):
    workOrder = mongo.db.workorders.find_one({'_id':ObjectId(id)})
    workOrder1 = mongo.db.workorders.find({'_id':ObjectId(id)}).count()
    print(workOrder1)
    resp = dumps(workOrder)
    app.logger.info('WorkOrder sucessfully displayed with id '+id)
    return resp

@app.route('/workOrder/delete/<id>', methods=['DELETE'])
@validate()
def workOrderDelete(id:str):
    mongo.db.workorders.delete_one({'_id':ObjectId(id)})
    resp = jsonify("The workOrder with Id " + id + " has been deleted")
    resp.status_code = 200
    app.logger.info('WorkOrder sucessfully deleted wit id '+id)
    return resp

@app.route('/workOrder/update/<id>', methods=['PUT'])
@validate()
def workOrderUpdate(body: WorkOrder,id: str ):
    _id = id
    _json = request.json
    _name = body.name
    _description = body.description
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
@validate()
def add_task(body: Task):
    _json = request.json
    _task_name = body.task_name
    _task_description = body.task_description
    _wordOrderId = body.wordOrderId
    

    if _task_name and mongo.db.workorders.find({"_id":ObjectId(_wordOrderId)}).count() == 1 and request.method == 'POST':
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
@validate()
def task(id: str):
    task = mongo.db.tasks.find_one({'_id':ObjectId(id)})
    resp = dumps(task)
    app.logger.info('Task sucessfully displayed with id '+id) 
    return resp


@app.route('/task/work/<id>')
@validate()
def task_workOrder(id: str):
    task = mongo.db.tasks.find_one({'wordOrderId':ObjectId(id)})
    resp = dumps(task)
    app.logger.info('Task sucessfully displayed with workOrder id '+id) 
    return resp    

@app.route('/task/delete/<id>', methods=['DELETE'])
@validate()
def taskDelete(id: str):
    mongo.db.tasks.delete_one({'_id':ObjectId(id)})
    resp = jsonify("The task with Id " + id + " has been deleted")
    resp.status_code = 200
    app.logger.info('task sucessfully deleted with id '+id) 
    return resp

# @app.route('/task/update/<tid>', methods=['PUT'])
# def taskUpdate(tid):
#     _id = tid
#     _json = request.json
#     _name = _json['name']
#     _description = _json['description']
#     _wordOrderId = _json['wordOrderId']
#     if _name and _id and request.method == 'PUT':
#         mongo.db.tasks.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':_name, 'description':_description,'wordOrderId':ObjectId(_wordOrderId)}})
#         resp = jsonify("task updated successfully")
#         resp.status_code = 200
#         return resp
#     else:
#         return not_found()

@app.route('/task/update/<id>', methods=['PUT'])
@validate()
def update_task(id: str, body: Task ):
    """
       Function to update the user.
       """
    try:
        # Get the value which needs to be updated
        try:
            _id = id
            _json = request.json
            _task_name = body.task_name
            _task_description = body.task_description
            _wordOrderId = body.wordOrderId
            _task_name and _id and request.method == 'PUT'
        except:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            app.logger.error('Bad request as the request body is not avalaible or wrong')
            return "Bad request as the request body is not avalaible or wrong", 400

        # Updating the user
        records_updated = mongo.db.tasks.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'task_name':_task_name, 'task_description':_task_description,'wordOrderId':ObjectId(_wordOrderId)}})
       

        # Check if resource is updated
        if records_updated.modified_count>0 :
            # Prepare the response as resource is updated successfully
            app.logger.info('Task sucessfully updated') 
            return "Task updated successfully", 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            app.logger.error('Bad Request 404 error') 
            return "Bad Request", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        app.logger.error('Task not found - Internal server error') 
        return "Internal Server Error", 500




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








    


        


    
