from datetime import datetime
from dateutil.relativedelta import relativedelta
import mongoconfig
from db import Database
from predict import Predict
from timeparser import TimeParser


def monthRangeFrom(months=0):
  return datetime.today() + relativedelta(months=months)

if __name__ == "__main__":
  # Connect to the database
  mongoDetails = mongoconfig.getMongoDetails()
  database = Database(mongoDetails["uri"], mongoDetails["port"], mongoDetails["database"])
  database.connect()
  # Get orders from three months ago.
  orders = database.getOrders(monthRangeFrom(months=-3))
  hourlyOrders = TimeParser.extractHourlyOrders(orders, monthRangeFrom(months=-3))
  database.close()
