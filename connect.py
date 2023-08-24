from pymongo import MongoClient
from pymongo.server_api import ServerApi

import redis

client = MongoClient(
    "mongodb+srv://vesnanifields:ZkzSOjxLQl5TYTpU@cluster0.pfhaw6o.mongodb.net/?retryWrites=true&w=majority",
    server_api=ServerApi('1')
    )

db = client.test
redis_client = redis.Redis(host="localhost", port=6379, password=None)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
