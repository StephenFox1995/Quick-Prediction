import os
import json


class Configuration(object):
  """
    Class to edit configuration file.
  """
  GMAPS_KEY = "gmaps"
  DATABASES = "databases"
  TOKEN = "token"

  _CONFIG_FILENAME = "config.json"
  _CONFIG_FILE_PATH = "/etc/quick/%s" % _CONFIG_FILENAME
  _CONFIG_DIR = "/etc/quick/"
  _MONGO_OBJECT_NAME = "mongodb"
  _MONGO_DATABASES = "databases"
  _GMAPS = "gmaps"
  _TOKEN = "token"
  _FILE_TEMPLATE = {"databases": []}

  @staticmethod
  def checkRoot():
    """
      Ensures that the user currently executing is the root user.
      @throws If not the root an exception is thrown
    """
    if os.getuid() != 0:
      raise Exception("Must be executed with root privileges.")


  def makeConfigFile(self):
    """
     Creates the configuration file where settings and configurations
     are stored.
    """
    Configuration.checkRoot()
    if not os.path.exists(self._CONFIG_DIR):
      os.mkdir(self._CONFIG_DIR)

    # Let user know that this configration file already exists
    # and that proceeding will overwrite the current configuration
    if os.path.exists(self._CONFIG_FILE_PATH):
      print("%s already exists. Overwrite? y/n" % self._CONFIG_FILE_PATH)
      response = raw_input()
      if response != "y":
        return
      print("Overwriting... %s" % self._CONFIG_FILE_PATH)
    with open(self._CONFIG_FILE_PATH, "w+") as fp:
      json.dump(self._FILE_TEMPLATE, fp, indent=2)
      print("Configuration file successfully created.")


  def addMongoDatabase(self, uri, port, database, username=None, password=None):
    """
      Adds basic details for a Mongo database to the configuration file.

      @param uri:(str) The URI to find the database.

      @param port:(int) The port the MongoDB instance is running on.

      @param database:(str) The name of the database to connect to.

      @param username:(str) The username.

      @param password:(str) The password.
    """
    fileContents = self.__readConfigFile()
    newDatabase = {"uri": uri, "port": port, "database": database}

    if username != None and password != None:
      newDatabase["username"] = username
      newDatabase["password"] = password

    fileContents[self._MONGO_DATABASES].append(newDatabase)
    self.__writeConfigFile(fileContents)

  def deleteMongoDatabase(self, uri, port, database):
    """
      Removes details for a database, from the databases list in the
      configuration file.

      @param uri:(str) The database uri.

      @param port:(int) The port.

      @param database:(str) The name of the database.
    """
    fileContents = self.__readConfigFile()
    databases = fileContents[self._MONGO_DATABASES]
    dbToCheck = {"uri": uri, "port": port, "database": database}
    for (i, value) in enumerate(databases):
      if (self.__dbCompare(value, dbToCheck)):
        del databases[i]
    print(databases)

    fileContents[self._MONGO_DATABASES] = databases
    self.__writeConfigFile(fileContents)

  def __dbCompare(self, db1, db2):
    """
      Compares the details of two databases, to check if they are the same.
    """
    if db1["uri"] == db2["uri"] and \
        db1["port"] == db2["port"] and \
        db1["database"] == db2["database"]:
      return True
    else:
      return False


  def addGoogleMapsKey(self, key):
    """
      Adds a Google Maps API key to the configuration file.

      @param key:(str) The Google Maps API key to add to the configuration file.
    """
    fileContents = self.__readConfigFile()
    fileContents[self._GMAPS] = key
    self.__writeConfigFile(fileContents)

  def deleteGoogleMapsKey(self):
    """
      Deletes the Google Maps API key in the configuration file
    """
    fileContents = self.__readConfigFile()
    del fileContents[self._GMAPS]
    self.__writeConfigFile(fileContents)


  def addTokenSecretKey(self, secret):
    """
      Adds the token secret to the configuration file.

      @param secret:(str) The token secret key.
    """
    fileContents = self.__readConfigFile()
    newTokenSecret = {"secret": secret}
    fileContents[self._TOKEN] = newTokenSecret
    self.__writeConfigFile(fileContents)


  def deleteTokenSecretKey(self):
    """
      Deletes the token secret from the configuration file.
    """
    fileContents = self.__readConfigFile()
    del fileContents[self._TOKEN]
    self.__writeConfigFile(fileContents)

  def read(self, prop):
    """
      Reads a property or properties from the config file.
      If the property exists it will be returned, otherwise if
      the property doesn't exist then the method will silently fail
      and None will be returned.

      @param prop:(list) The property or properties to retrieve.
      @return list of the properties.
    """
    fileContents = self.__readConfigFile()
    if isinstance(prop, list):
      data = []
      for p in prop:
        if p in fileContents:
          data.append(fileContents[p])
      return data
    raise ValueError("Expected type 'list' got %s" % type(prop))

  def __readConfigFile(self):
    """
      Read from the configuration file defined by __CONFIG_FILE_PATH.
    """
    with open(self._CONFIG_FILE_PATH) as fp:
      return json.load(fp)


  def __writeConfigFile(self, contents):
    """
      Write to the configuration file defined by __CONFIG_FILE_PATH.
      Note: must have root priveleges.
    """
    Configuration.checkRoot()
    with open(self._CONFIG_FILE_PATH, "w+") as fp:
      contents = json.dumps(contents, indent=2, sort_keys=True)
      fp.write(contents)
