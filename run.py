import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from quickprediction.dbs.orderdb import OrderDB
from quickprediction.dbs.predictiondb import PredictionDB
from quickprediction.prediction.predict import Predict
from quickprediction.parsers.timeparser import TimeParser
from quickprediction.config import Configuration


def monthRangeFrom(months=0):
  return datetime.today() + relativedelta(months=months)


def args():
  parser = argparse.ArgumentParser("Execute swarms and models.")
  parser.add_argument(
    "-s", "--swarmtype",
    help="The swarm type to perform.",
    dest="swarmtype",
    choices=set(("orderamount", "producttype"))
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
  return parser


if __name__ == "__main__":
  args = args().parse_args()
  swarmType = args.swarmtype.upper()
  businessid = args.businessid
  directory = args.dir

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
  # Parse out the number of orders for each hour of the last three months.
  hourlyOrders = TimeParser.extractHourlyOrders(orders, monthsprior)
  orderDB.close()
  # Get ready to write to .csv file
  predict = Predict(businessid, swarmType, directory)
  rows = predict.begin(hourlyOrders)

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