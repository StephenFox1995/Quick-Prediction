from .database import Database


class PredictionDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(PredictionDB, self).__init__(uri, port, dbName, user, password)


  def write(self, businessID, swarmType, data):
    predictionData = {
      "businessID": businessID,
      "swarmType": swarmType,
      "data": data
    }
    self._database.prediction.insert(predictionData)
