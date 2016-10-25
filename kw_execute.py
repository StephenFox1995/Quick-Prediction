from qswarm import QSwarm
from qrunner import QRunner

from sources.kw_swarm_description import SWARM_DESCRIPTION
import os
import datetime

DATE_TIME_FORMAT = "%m/%d/%y %H:%M"
CSV_FILE = "sources/kw_usage.csv"
MODEL_NAME = "kw_energy_consumption"

def rowsToParse(row):
  timestamp = datetime.datetime.strptime(row[0], DATE_TIME_FORMAT)
  kw_energy_consumption = float(row[1])
  return {
    "timestamp": timestamp,
    "kw_energy_consumption": kw_energy_consumption
  }


if __name__ == "__main__":
  qswarm = QSwarm(SWARM_DESCRIPTION)
  qswarm.start("kw_swarm")
  
  try: 
    from swarm.kw_swarm_model_params import kw_swarm_model_params
    qrunner = QRunner()
    qrunner.createModel(kw_swarm_model_params.MODEL_PARAMS, "kw_energy_consumption")
    inputFilePath = os.path.abspath("swarm")
    qrunner.runModel(MODEL_NAME, CSV_FILE, 3, rowsToParse)
  except ImportError:
    print("Error trying to run model. swarm_model_params file could not be found.")
  



