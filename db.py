from pymongo import MongoClient

class Database(object):
  # Gets a connection to the database.
  
  def __init__(self, uri, port, database):
    self.uri = uri
    self.port = port
    self.dbName = database
    
  def connect(self):
    """
    Connects to the database from the arguments specified in the constructor.
    """
    self.connectionString = self.__createConnectionString(self.uri, self.port, self.dbName)
    self.client = MongoClient(self.connectionString)
    self.database = self.client.get_database(self.dbName)
    
  def close(self):
    """
    Closes the current connection to the database.
    """
    self.client.close()
    
  def __createConnectionString(self, uri, port, database):
    """
    Creates connection to the database.
    """
    return "mongodb://%s:%s/%s" % (uri, port, database)
  
  # Get orders from the database connection for this class.
  def getOrders(self, fromDate):
    """
    Get orders from the databases starting at the fromDate argument.
    @param fromDate:(datetime.datetime) The start date to get the order froms.
    """
    return self.database.orders.find({"createdAt": {"$gte": fromDate}})
