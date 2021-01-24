import json

from flask import Blueprint, request, Response

from mongo.custom_mongo import Mongo_Handler

def mongo_manager_bp():
    mongo_manager_bp = Blueprint('mongo_manager_bp', __name__)
    mongo = Mongo_Handler()
    @mongo_manager_bp.route("/articles/", methods=["PUT", "POST", "GET"])
    def article_insert():
        '''
        PUT/POST will create or insert a policy in the repository
        Mandatory parameters:
    
        '''
        print("Processing " + request.method)
        response = Response()
        mongo = Mongo_Handler()
        a=mongo.get_article_from_id("600bfb3dd67f0394c30ca310")
        print(a)
        return response
        #Insert once is authorized
      
            
    @mongo_manager_bp.route("/articles/<article_id>", methods=["GET", "PUT", "POST", "DELETE"])
    def policy_operation(article_id):
        '''
        PUT/POST will update a policy in the repository by its _id
        GET will return the policy by its _id or by specifying the resource_id on the body
        DELETE will delete the policy by its _id
        This endpoint will check the headers of the request to retrieve a token
        To operate against any policy the UUID of the user must match with the one associated to the policy
        Mandatory parameters:
            - endpoint: <DOMAIN>/policy/<policy_id>    <-   The policy_id can be specify with both formats: [policy_id/ObjectId(policy_id)]
            - headers(JWT_id_token/OAuth_access_token): to verify the user credentials
            - body(policy_data_model): Only for the GET/PUT/POST, As a dicionary/json.
        '''
        print("Processing " + request.method + " policy request...")
        response = Response()
        mongo = Mongo_Handler()

    return mongo_manager_bp, mongo
