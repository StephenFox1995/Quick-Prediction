import json

def getMongoDetails():
  with open("/etc/quick/config") as configFile:
    config = json.load(configFile)
    return config["mongodb"]
