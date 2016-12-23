import json

def getMongoDetails():
  """
  Returns the connection details that are in the file /etc/quick.config.
  @return dict with the mongoDetails 
    {
      "uri": "x",
      "port": "x",
      "database": "x"
    }
  """
  with open("/etc/quick/config") as configFile:
    config = json.load(configFile)
    return config["mongodb"]
