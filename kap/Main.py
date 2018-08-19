"""It is to run the whole crawler"""
import time
from pymongo import MongoClient
from Kap import Kap


# setting up mongoDB
client = MongoClient()
db = client.web
collection = db.kap

kap = Kap()  # initializing the crawler
kap.update(collection)  # updating the system

# time.sleep(15)  # optional pause

kap.export_to_json("extracted_data\\notifications.json", collection)
