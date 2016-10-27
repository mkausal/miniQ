import pymongo


class MongoWrapper(object):
    _shared_state = {}
    db_conn_map = {}

    def __init__(self):
        self.__dict__ = self._shared_state

    def mongo_db_connect(self, server_key='localhost', database='miniQ'):
        mongo_conn = pymongo.MongoClient(host=server_key, w=0)
        mongo_db = mongo_conn[database]
        return mongo_db

    def get_mongo_collection(self, collection_name, database='miniQ', server_key='localhost'):
        mongo_db = self.mongo_db_connect(server_key, database)
        return mongo_db[collection_name]
