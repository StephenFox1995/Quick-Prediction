from pymongo import MongoClient

class Database(object):
  # Gets a connection to the database.
  
  def __init__(self, uri, port, database):
    self.uri = uri
    self.port = port
    self.dbName = database
    
  # Connect to the database.
  def connect(self):
    self.connectionString = self._createConnectionString(self.uri, self.port, self.dbName)
    self.client = MongoClient(self.connectionString)
    self.database = self.client.get_database(self.dbName)
    
  def close(self):
    self.client.close()
  
  # Creates connection appopriate url for connection to mongodb.
  def _createConnectionString(self, uri, port, database):
    return "mongodb://%s:%s/%s" % (uri, port, database)
  
  # Get orders from the database connection for this class.
  def getOrders(self, fromDate):
    return self.database.orders.find({"createdAt": {"$gte": fromDate}})
