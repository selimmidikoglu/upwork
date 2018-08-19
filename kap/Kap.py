import json
from bson import json_util
from pymongo import MongoClient
from pymongo.collection import Collection

from NotificationExtractor import parse_source_code
from SourceCodeExtractor import get_source_code


class Kap:
    """A System to extract data from kap.org.tr"""

    @staticmethod
    def export_to_json(path: str, collection: Collection):
        """To export the newly found data to a json file"""

        data = []
        for notf in collection.find():
            data.append(notf)

        data = json.dumps(data, default=json_util.default)
        with open(path, encoding='utf-8', mode='w+') as f:
            f.write(data)

    @staticmethod
    def export_from_json(path: str, collection: Collection):
        """To export daa from a json file and write it to a collection"""

        with open(path, encoding='utf-8', mode='r') as f:
            data = f.read()

        data = json.loads(data, object_hook=json_util.object_hook)
        for item in data:
            try:
                collection.insert_one(item)
            except:
                print("Already exists")

    @staticmethod
    def update(end : int):
        """Gets new notifications and updates mongoDB"""

        print("Updating Kap..")

        # connecting to MongoDB
        client = MongoClient()
        db = client.web
        collection = db.kap

        # beginning index of notifications
        begin = collection.find_one({'_id': 1})["max_id"]

        # this should be updated
        # end = 621000

        # getting source code
        get_source_code(begin, end)

        # parsing source codes
        parse_source_code(begin, end, collection)

        print("Updating done!")

if __name__ == '__main__':
    # connecting to MongoDB
    client = MongoClient()
    db = client.web
    collection = db.kap

    Kap.update(620400)
