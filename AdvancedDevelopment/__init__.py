import pymongo
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

# cluster = MongoClient("mongodb+srv://s5124723:UJZ6xxtNrnYwSNWowyz8@advanceddevelopment.aiiro.mongodb.net/test")
# db = cluster["AdvancedDevelopment"]
# collection = db["test"]

# try:
#     post1 = {"_id": 1, "name": "Lucas", "score": 5}
#     post2 = {"_id": 2, "name": "Daniel", "score": 5}
#     collection.insert_many([post1, post2])
# except BulkWriteError as bwe:
#     print(bwe)
#
