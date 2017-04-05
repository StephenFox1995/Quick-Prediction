import argparse
from datetime import datetime
from quickprediction.prediction import swarmtype
from dateutil.relativedelta import relativedelta
from quickprediction.dbs.orderdb import OrderDB
from quickprediction.dbs.predictiondb import PredictionDB
from quickprediction.prediction.predict import Predict
from quickprediction.config import Configuration
from quickprediction.parsers.timeparser import *

def monthRangeFrom(months=0):
  return datetime.now() + relativedelta(months=months)


def args():
  parser = argparse.ArgumentParser("Execute swarms and models.")
  parser.add_argument(
    "-s", "--swarmtype",
    help="The swarm type to perform.",
    dest="swarmtype",
    choices=set(("orderamount", "expectedemployees"))
  )
  parser.add_argument(
    "-b", "--businessid",
    help="The id of the business.",
    dest="businessid"
  )
  parser.add_argument(
    "-m", "-monthsprior",
    help="How far back data from the database should be fetched in months for swarming.",
    dest="monthsprior",
    type=int,
    default=-3
  )
  parser.add_argument(
    "-d", "--dir",
    help="The base directory to write the files to. \
      If the directory does not exists, it will be created.",
    dest="dir"
  )
  parser.add_argument(
    "--multitask",
    help="The multitask value",
    dest="multitask"
  )
  return parser


if __name__ == "__main__":
  args = args().parse_args()
  swarmType = args.swarmtype.upper()
  businessid = args.businessid
  directory = args.dir
  multitask = args.multitask
  monthsprior = monthRangeFrom(args.monthsprior)

  config = Configuration()
  dbDetails = config.read([Configuration.DATABASES])[0][0]
  # Connect to the database
  orderDB = OrderDB(
    dbDetails["uri"],
    dbDetails["port"],
    dbDetails["database"],
    dbDetails["username"],
    dbDetails["password"]
  )
  orderDB.connect()
  # Get orders from three months ago.
  orders = orderDB.read(fromDate=monthsprior)
  predictData = None

  if swarmType == swarmtype.ORD_AMOUNT:
    # Parse out the number of orders for each hour of the last x months.
    predictData = extractHourlyOrders(orders, monthsprior)
  elif swarmtype.EXPECTED_EMPLOYEES:
    # Parse out the number of conflicts for each hour of the last x months.
    predictData = extractHourlyConflicts(orders, monthsprior, multitask=multitask)
  orderDB.close()

  # Get ready to write to .csv file
  predict = Predict(businessid, swarmType, directory)
  rows = predict.begin(predictData)

  print("Writing to database...")
  predictionDB = PredictionDB(
    dbDetails["uri"],
    dbDetails["port"],
    dbDetails["database"],
    dbDetails["username"],
    dbDetails["password"]
  )
  predictionDB.connect()
  predictionDB.write(businessid, swarmType, rows)
  print("Done!")