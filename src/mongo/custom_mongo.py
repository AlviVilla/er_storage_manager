#!/usr/bin/env python3
import pymongo
import json
from bson.objectid import ObjectId

class Mongo_Handler:

    def __init__(self, **kwargs):
        self.modified = []
        self.__dict__.update(kwargs)
        
        self.myclient = pymongo.MongoClient('localhost', 27017)
        self.db = self.myclient["entorno_rural"]

    def create_json(self, data):
        '''
        Creates a template of policy to insert in the database
        '''
        y = json.dumps(data)
        return j

    def insert_document(self, data):
        '''
            Generates a document with json format (name: str, description: str, id: str,cfg: dict, scopes:list ): 
                -NAME: Name generic for the policy
                -DESCRIPTION: Custom description for the policy pourpose
                -ID: Unique ID for the policy
                -POLICY_CFG: Custom rules for the policy configuration
                -SCOPES: List of scopes for the policy
            Check the existence of the policy to be registered on the database
            If alredy registered will update the values
            If not registered will add it and return the query result
        '''
        dblist = self.myclient.list_database_names()
        # Check if the database alredy exists
        if "entorno_rural" in dblist:
            col = self.db['entorno_rural']
            myres = self.create_json(data)
            x=None
            if self.exists(name=name, col=col):
                print('alredy exists')
                return None
            # Add the resource since it doesn't exist on the database
            else:
                x = col.insert_one(myres)
                return 'New Article with ID: ' + str(x.inserted_id)
        else:
            col = self.db['entorno_rural']
            myres = self.create_json(data)
            x = col.insert_one(myres)
            return 'New Document with ID: ' + str(x.inserted_id)

    def delete_document(self, _id):
        '''
            Check the existence of the resource inside the database
            And deletes the document
        '''
        if self.exists(_id=_id):
            col = self.db['entorno_rural']
            myId=self.parse_id(_id)
            myquery = { "_id": myId }
            a= col.delete_one(myquery)
    
    def update_document(self, _id, dict_data):
        '''
        Find the resource in the database by id, add or modify the changed values for the resource.
        '''
        col = self.db['entorno_rural']
        myid = self.parse_id(_id)
        if self.exists(_id=_id):
            myquery= {'_id': myid}
            new_val= {"$set": dict_data}
            x = col.update_many(myquery, new_val)
            if x.modified_count == 1:
                return 'Updated'
            elif x.modified_count == 0:
                return 'No changes made'
            return str(x.modified_count)
        else:
            return print('Can not update the policy, it does not exist')
             

    def get_id_from_name(self, name:str):
        col= self.db['entorno_rural']
        myquery={'name': name}
        found=col.find_one(myquery)
        if found:
            return found['_id']
        else: return None

    def parse_id(self, _id):
        myId=None
        if 'ObjectId' in str(_id):
            if type(_id) == str:
                a=_id[_id.find("(")+1:_id.find(")")]
                myId = ObjectId(str(a))
            else:
                myId = _id
        else:
            myId = ObjectId(_id)
        return myId

    def get_all(self):
        '''
            Finds all documents
        '''
        col= self.db['entorno_rural']
        myquery= {}
        found=col.find(myquery)
        if found:
            return found
        else: return None
    
    def get_document_from_id(self, _id):
        '''
            Finds the article by its id
            Returns the policy in json format
        '''
        col= self.db['entorno_rural']
        myId=self.parse_id(_id)
        myquery= {'_id': myId}
        found=col.find_one(myquery)
        if found:
            return found
        else: return None


    def exists(self, _id=None, name=None, col=None):
        '''
            Check the existence of the resource inside the database by looking for the id or the name
            Input:  
                -_id: Search the _id inside the database
                -name:
            Return boolean result
        ''' 
        if _id:
            myquery = {"_id": _id}
        else:
            myquery = { "name": name }

        if col.find_one(myquery): return True
        else: return False
       
            
