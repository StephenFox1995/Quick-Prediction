from qswarm import QSwarm
from qrunner import QRunner

from sources.swarm_description import SWARM_DESCRIPTION
import os
import datetime

DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
CSV_FILE = "sources/previous_three_months_out.csv"
MODEL_NAME = "orders"

def rowsToParse(row):
  timestamp = datetime.datetime.strptime(row[0], DATE_TIME_FORMAT)
  purchase = int(row[1])
  return {
    "timestamp": timestamp,
    "orders": purchase
  }



if __name__ == "__main__":
  qswarm = QSwarm(SWARM_DESCRIPTION)
  qswarm.start("orders_swarm")
  
  try: 
    from swarm.orders_swarm_model_params import orders_swarm_model_params
    qrunner = QRunner()
    qrunner.createModel(orders_swarm_model_params.MODEL_PARAMS, "orders")
    inputFilePath = os.path.abspath("swarm")
    qrunner.runModel("orders", CSV_FILE, 3, rowsToParse)
  except ImportError:
    print("Error trying to run model. swarm_model_params file could not be found.")