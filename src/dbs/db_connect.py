import pymongo

from src.configs.index import MONGO_URI, DB_NAME


def get_db_connection():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[DB_NAME]
    if db is None:
        raise Exception("Could not connect to the database")
    else:
        print("Connected to the database")
    return db
