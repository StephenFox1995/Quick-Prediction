from datetime import datetime
from dateutil.relativedelta import relativedelta
from db import Database
from predict import Predict
from timeparser import TimeParser
import swarmtype
import argparse

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
        help="The base directory to write the files to. If the directory does not exists, it will be created.",
        dest="dir"
  )
  parser.add_argument(
    "-uri",
        help="The uri to connect to the mongo database in the format: 'mongodb://uri:port/database'",
        dest="mongoURI"
  )
  parser.add_argument(
    "-db", "-dbName",
        help="The name of the Mongo database to retrieve the orders from.",
        dest="dbName"
  )
  return parser


if __name__ == "__main__":
  args = args().parse_args()
  swarmType = args.swarmtype.upper()
  businessid = args.businessid
  directory = args.dir
  mongoURI = args.mongoURI
  dbName = args.dbName


  monthsprior = monthRangeFrom(args.monthsprior)
  # Connect to the database
  database = Database(mongoURI, dbName)
  database.connect()
  # Get orders from three months ago.
  orders = database.getOrders(monthsprior)
  # Parse out the number of orders for each hour of the last three months.
  hourlyOrders = TimeParser.extractHourlyOrders(orders, monthsprior)
  database.close()
  # Get ready to write to .csv file
  predict = Predict(businessid, swarmType, directory)
  predict.begin(hourlyOrders)