from .database import Database
from bson.objectid import ObjectId
import quickprediction.prediction.swarmtype as swarmtype
class PredictionDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(PredictionDB, self).__init__(uri, port, dbName, user, password)


  def write(self, businessID, swarmType, data):
    predictionData = {
      "businessID": ObjectId(businessID),
      "swarmType": swarmType,
      "data": data
    }
    self._database.predictions.remove({"$and": [{"businessID":  ObjectId(businessID)}, {"swarmType": swarmType}]})
    self._database.predictions.insert(predictionData)
