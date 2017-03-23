from pymongo import MongoClient
from . import mongoutil

class Database(object):
  class InvalidConnectionError(Exception):
    pass

  def __init__(self, uri, port, dbName, user=None, password=None):
    self._uri = uri
    self._port = port
    self._dbName = dbName
    self.__user = user
    self.__password = password
    self.__connectionString = mongoutil.connString(uri, port, dbName, user, password)
    self._connected = False
    self._client = None
    self._database = None

  def connect(self):
    """
      Connects to the database from the arguments specified in the constructor.
    """
    self._client = MongoClient(self.__connectionString)
    self._database = self._client.get_database(self._dbName)
    self._connected = True
    del self.__user
    del self.__password
    del self.__connectionString

  def close(self):
    """
      Closes the current connection to the database.
    """
    self._client.close()

  def read(self):
    """
      As each subclass will have their own read() functionality, this method is only provided
      for error checking.
    """
    if not self._connected:
      raise Database.InvalidConnectionError(
        "No connection established, please invoke connect() method."
      )

