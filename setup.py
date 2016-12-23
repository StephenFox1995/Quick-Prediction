from datetime import datetime
from dateutil.relativedelta import relativedelta
import mongoconfig
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
          help="The swarm type to perform [orderamount, producttype]", 
          dest="swarmtype", 
          choices=set(("orderamount", "producttype"))
  )
  parser.add_argument(
    "-b", "--businessid",
        help="The id of the business",
        dest="businessid"
  )
  return parser


if __name__ == "__main__":
  args = args().parse_args()
  swarmType = args.swarmtype.upper()
  businessid = args.businessid

  # Connect to the database
  mongoDetails = mongoconfig.getMongoDetails()
  database = Database(mongoDetails["uri"], mongoDetails["port"], mongoDetails["database"])
  database.connect()
  # Get orders from three months ago.
  orders = database.getOrders(monthRangeFrom(months=-3))
  # Parse out the number of orders for each hour of the last three months.
  hourlyOrders = TimeParser.extractHourlyOrders(orders, monthRangeFrom(months=-3))
  database.close()
  # Get ready to write to .csv file
  predict = Predict(businessid, swarmType)
  predict.begin(hourlyOrders)