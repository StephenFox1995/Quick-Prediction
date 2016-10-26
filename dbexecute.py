from db import Database
from bson.objectid import ObjectId
from qoutput import QOutput
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time


# current date  -3 months, do each quarter.

DATE_TIME_FORMAT = "%d/%m/%Y %H:%M"
DATE_FORMAT = "%d/%m/%Y"
HOUR_FORMAT = "%H"

def extractTime(previous, current):
  previous.append(current["createdAt"])
  return previous

def currentDate():
  return time.strftime("%d/%m/%Y")

def threeMonthsAgo():
  return datetime.today() + relativedelta(months=-3)


database = Database()
db = database.getDB()

# Get the orders from the database
orders = db.orders.find({"createdAt": {"$gte": threeMonthsAgo()}})


# Build up rows for .csv file
rows = []
ordersArray = []
# Add all orders to ordersArray
for order in orders:
  ordersArray.append(order)

# Get all timestamps
orderTimeStamps = reduce(extractTime, ordersArray, [])



def getOrdersForDay(day, orders):
  """
  Get amount of orders for a day. This function calculates this
  by checking if there is two objects in the array with the same
  date. If the objects have the same date, then they are assumed
  to be an order for that day, thus get added to the array.
  """
  def filterDays(dayToCompare):
    dateOne = datetime.strftime(day, DATE_FORMAT)
    dateTwo = datetime.strftime(dayToCompare, DATE_FORMAT)  
    if dateOne == dateTwo:
      return dateTwo
  filtered = filter(filterDays, orders)
  return filtered 


def getOrdersForHour(hour, orders):
  def filterHours(hourToCompare):
    hourOne = datetime.strftime(hour, HOUR_FORMAT)
    hourTwo = datetime.strftime(hourToCompare, HOUR_FORMAT)
    if hourOne == hourTwo:
      return hourTwo
  filtered = filter(filterHours, orders)
  return filtered
     


ordersForDay = getOrdersForDay(orderTimeStamps[34], orderTimeStamps)

print(len(getOrdersForHour(ordersForDay[5], ordersForDay)))