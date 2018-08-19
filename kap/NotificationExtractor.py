import time
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from Notification import Notification


def parse_source_code(begin: int, end: int, destination: Collection):
    """This method is for parsing the source codes stored by SourceCodeExtractor.py"""

    print("Parsing source code..")

    companies_to_check = ["AKBNK", "GARAN", "BIMAS", "TUPRS", "TCELL", "SAHOL", "ISCTR", "EREGL", "KCHOL",
                          "HALKB", "EKGYO", "THYAO", "ARCLK", "VAKBN", "PETKIM", "YKBNK", "TOASO",
                          "SISE", "ASELS", "ENKA", "ULKER", "TTKOM", "TAVHL", "FROTO", "SODA", "TKFEN",
                          "KRDMD", "MAVI", "KOZAL", "BIST30", "BIST100", "BORSAISTANBUL"]

    # connecting to MongoDB
    client = MongoClient()
    db = client.web
    collection = db.tmp

    notifications = []
    for i in range(begin, end + 1):
        # print info
        print(i, (i - begin) * 100 / (end - begin + 1), "%")

        # store notifications to mongoDB after every 200
        if i != begin and i % 200 == 0:
            for item in notifications:
                try:
                    destination.insert_one(item)
                except DuplicateKeyError:
                    print(item["_id"], "----This element already exists----")

                    # optional: comment out to override the data in database
                    # collection.delete_one({"_id": item["_id"]})
                    # collection.insert_one(item)
            notifications.clear()

        try:
            # get source code and parse it
            item = collection.find_one({"_id": i})
            notification = Notification(item["source_code"], item["_id"])

            # add to the list if it is about our companies
            for company in notification.related_companies:
                if company in companies_to_check:
                    notifications.append(notification.dump())
                    break

        except TypeError:  # if it is not found
            print(i, "---not found---")

    # store the remaining notifications
    for item in notifications:
        try:
            destination.insert_one(item)
        except DuplicateKeyError:
            print(item["_id"], "---This element already exists---")

            # optional: comment out to override the data in database
            # collection.delete_one({"_id": item["_id"]})
            # collection.insert_one(item)
    # storing the last parsed notifications index
    try:
        destination.insert_one({'_id': 1, 'max_id': end})
    except DuplicateKeyError:
        destination.delete_one({'_id': 1})
        destination.insert_one({'_id': 1, 'max_id': end})

    collection.drop()
    print("Parsing source code is done!")


if __name__=='__main__':
    client = MongoClient()
    db = client.web
    collection = db.kap

    ctime = time.time()

    parse_source_code(610000, 620000, collection) # 620974

    print("Time:", time.time() - ctime)
