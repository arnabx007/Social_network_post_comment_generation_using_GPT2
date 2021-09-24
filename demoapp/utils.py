# Set up pymongo and connect to MongoDB
from pymongo import MongoClient

def get_db(db_name:str, host=None, port:int=None , username:str=None, password:str=None):
    client = MongoClient(host=host,
                         port=port,
                         username=username,
                         password=password
                        )

    db = client[db_name]
    return db, client

def get_collection(db, collection_name):
    return db[collection_name]

