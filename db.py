from pymongo import MongoClient
from mongoconfig import getMongoDetails

class Database(object):
  def getDB(self):
    details = getMongoDetails()
    mongoString = "mongodb://%s:%s/%s" % (details["uri"], details["port"], details["database"])
    client = MongoClient(mongoString)
    return client.quick



