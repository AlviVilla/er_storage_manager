import json
from flask import Blueprint, request, Response
from mongo.custom_mongo import Mongo_Handler
from config import config_parser
g_config = config_parser.get_config()


def mongo_manager_bp():
    mongo_manager_bp = Blueprint('mongo_manager_bp', __name__)
    mongo = Mongo_Handler()
    @mongo_manager_bp.route("/mongo/", methods=["PUT", "POST", "GET"])
    def article_insert():
        '''
        GET will retrieve a list of documents
        PUT/POST will create or insert a document in the repository
        Mandatory parameters:
    
        '''
        response = Response()
        mongo = Mongo_Handler()
        if request.method == "GET":   
            list_of_docs={}
            a= mongo.get_all()
            list_of_docs['docs'] = a
            for n in list_of_docs['docs']:
                if '_id' in n:
                    n['_id'] = str(n['_id'])
            return json.dumps(list_of_docs)
        else:
            if request.is_json:
                data = request.get_json()
                if data.get("name"):
                    return mongo.insert_document(data)
                else:
                    response.status_code = 400
                    response.headers["Error"] = "Bad Request: Invalid data or incorrect format!"
                    return response

            
    @mongo_manager_bp.route("/mongo/<doc_id>", methods=["GET", "PUT", "POST", "DELETE"])
    def article_operation(doc_id):
        '''
        PUT/POST will update a doc in the repository by its _id
        GET will return the doc by its _id or by specifying the resource_id on the body
        DELETE will delete the doc by its _id
        This endpoint will check the headers of the request to retrieve a token
        To operate against any doc the UUID of the user must match with the one associated to the doc
        Mandatory parameters:
            - endpoint: <DOMAIN>/mongo/<doc_id>    <-   The doc_id can be specify with both formats: [doc_id/ObjectId(doc_id)]
            - body(doc_data_model): Only for the GET/PUT/POST, As a dicionary/json.
        '''
        print("Processing " + request.method + " doc request...")
        response = Response()
        mongo = Mongo_Handler()
        if request.method == "POST" or request.method == 'PUT':
            if request.is_json:
                data = request.get_json()
                if data.get("name"):
                    return mongo.update_document(doc_id, data)
                else:
                    response.status_code = 500
                    response.headers["Error"] = "Invalid data or incorrect format!"
                    return response

        elif request.method == "GET":
            
            a= mongo.get_document_from_id(doc_id)
            a['_id'] = str(a['_id'])
            return json.dumps(a)
        #Deletes a doc by its _id
        elif request.method == "DELETE":
            mongo.delete_document(doc_id)
            response.status_code = 204
            response.text = 'DELETED'
            return response
        else:
            response.status_code = 500
            response.headers["Error"] = "Method not allowed"
            return response

    @mongo_manager_bp.route("/tags/", methods=["GET"])
    def get_tags():
        '''
        GET will retrieve a list of tagss
    
        '''
        response = Response() 

        if g_config["tag_list"]:
            return {"tag_list": g_config["tag_list"] }
        else:
            response.status_code = 400
            response.headers["Error"] = "No data in config"
            return response



    return mongo_manager_bp, mongo
