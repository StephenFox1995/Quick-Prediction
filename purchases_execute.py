from qswarm import QSwarm
from qrunner import QRunner

from sources.swarm_description import SWARM_DESCRIPTION
import os
import datetime

DATE_TIME_FORMAT = "%m/%d/%Y %H:%M"
CSV_FILE = "sources/purchases_hourly.csv"
MODEL_NAME = "purchases"

def rowsToParse(row):
  timestamp = datetime.datetime.strptime(row[0], DATE_TIME_FORMAT)
  purchase = int(row[1])
  return {
    "timestamp": timestamp,
    "purchases": purchase
  }



if __name__ == "__main__":
  qswarm = QSwarm(SWARM_DESCRIPTION)
  qswarm.start("purchases_swarm")
  
  try: 
    from swarm.purchases_swarm_model_params import purchases_swarm_model_params
    qrunner = QRunner()
    qrunner.createModel(purchases_swarm_model_params.MODEL_PARAMS, "purchases")
    inputFilePath = os.path.abspath("swarm")
    qrunner.runModel("purchases", CSV_FILE, 3, rowsToParse)
  except ImportError:
    print("Error trying to run model. swarm_model_params file could not be found.")