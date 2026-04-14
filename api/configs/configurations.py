import pymongo
import dotenv
import os

dotenv.load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB = os.getenv('MONGO_DB')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')


class Database:
    def __init__(self, collection_name=None):
        self.client = pymongo.MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB]
        if collection_name:
            self.collection = self.db[collection_name]
        else:
            self.collection = self.db[Config.MONGO_COLLECTION]

    def insert(self, data):
        return self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)

    def find_one(self, query):
        return self.collection.find_one(query)

    def update(self, query, data):
        return self.collection.update_one(query, data)

    def delete(self, query):
        return self.collection.delete_one(query)

    def close(self):
        self.client.close()