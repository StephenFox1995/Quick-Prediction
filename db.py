from pymongo import MongoClient

class Database(object):
  def __init__(self, uri, dbName):
    self._uri = uri
    self._dbName = dbName

  def connect(self):
    """
    Connects to the database from the arguments specified in the constructor.
    """
    self.client = MongoClient(self._uri)
    self.database = self.client.get_database(self._dbName)
    
  def close(self):
    """
    Closes the current connection to the database.
    """
    self.client.close()
    
  def createConnectionString(self, uri, port, database):
    """
    Creates the approriate uri to connect to the database.
    """
    return "mongodb://%s:%s/%s" % (uri, port, database)
  
  # Get orders from the database connection for this class.
  def getOrders(self, fromDate):
    """
    Get orders from the databases starting at the fromDate argument.
    @param fromDate:(datetime.datetime) The start date to get the order froms.
    """
    return self.database.orders.find({"createdAt": {"$gte": fromDate}})
