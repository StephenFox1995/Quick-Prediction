from db import Database
from bson.objectid import ObjectId
from qoutput import QOutput
from datetime import datetime
from dateutil.relativedelta import relativedelta



# current date  -3 months, do each quarter.

# hours in datetime format
hours = map(lambda hour: datetime.strptime(hour, "%H:%M") ,[
  "00:00",
  "01:00",
  "02:00",
  "03:00",
  "04:00",
  "05:00",
  "06:00",
  "07:00",
  "08:00",
  "09:00",
  "10:00",
  "11:00",
  "12:00",
  "13:00",
  "14:00",
  "15:00",
  "16:00",
  "17:00",
  "18:00",
  "19:00",
  "20:00",
  "21:00",
  "22:00",
  "23:00"
])


def threeMonthsAgo():
  return datetime.today() + relativedelta(months=-3)


def dateRange(start, end, increment, period):
# http://stackoverflow.com/a/10688309/2875074
    result = []
    nxt = start
    delta = relativedelta(**{period:increment})
    while nxt <= end:
        result.append(nxt)
        nxt += delta
    return result


def getOrdersForDate(date, orders):
  """
  Get amount of orders for a day. This function calculates this
  by checking if there is two objects in the array with the same
  date. If the objects have the same date, then they are assumed
  to be an order for that day, thus get added to the array.
  @param day: () The day to filter with the dataset.
  @param orders: (array) The dataset of orders. 
  """
  def filterDays(dayToCompare):
    DATE_FORMAT = "%d/%m/%Y"
    dateOne = datetime.strftime(date, DATE_FORMAT)
    dateTwo = datetime.strftime(dayToCompare, DATE_FORMAT)  
    if dateOne == dateTwo:
      return dateTwo
  return filter(filterDays, orders) 


def getOrdersForHour(hour, orders):
  """
  Returns all orders for a given hour within a dataset.
  Note if there are many days within the dataset then this function
  will return all occurences of that hour for all days.
  @param hour: () The hour to filter the dataset by.
  @param orders: (array) The dataset of orders.
  """
  def filterHours(hourToCompare):
    HOUR_FORMAT = "%H"
    hourOne = datetime.strftime(hour, HOUR_FORMAT)
    hourTwo = datetime.strftime(hourToCompare, HOUR_FORMAT)
    if hourOne == hourTwo:
      return hourTwo
  return filter(filterHours, orders)


def getAllUniqueDates(dates):
  DATE_FORMAT = "%d/%m/%Y"
  
  return map(lambda c: datetime.strptime(c, DATE_FORMAT), \
    reduce(lambda l, x: l.append(datetime.strftime(x, DATE_FORMAT))  
      or l if datetime.strftime(x, DATE_FORMAT) not in l else l, dates, []))


def getDateTimesFromMongoOrderData(orders):
  def extractTime(current):
    return current["createdAt"]
  # Get all timestamps from mongo
  return  map(extractTime, orders)

def zeroFillOrdersForFullDay(date):
  return map(lambda hour: {"hour": datetime.combine(date, datetime.time(hour)), "amount": 0}, hours)
  


database = Database()
db = database.getDB()

# Get the orders from the database
orders = db.orders.find({"createdAt": {"$gte": threeMonthsAgo()}})
# Get all date times from orders
orderDates = getDateTimesFromMongoOrderData(orders)
# Get every date between today and three months ago.
threeMonthDateRange = dateRange(threeMonthsAgo(), datetime.today(), 1, 'days')

# All the details about orders for the previous three months.
orderDetailsForThreeMonths = []

# Loop through array of dates from previous three months
# check the amount of orders per hour and add to dict.
for date in threeMonthDateRange:
  orderDetails = {
    "date": object,
    "orders": []
  }
  orderDetails["date"] = date

  ordersForDate = getOrdersForDate(date, orderDates)
  # if the order amount for that date is zero then just fill all hours with a order count of 0
  if len(ordersForDate) == 0:
    orderDetails["orders"] = zeroFillOrdersForFullDay(date)
    orderDetailsForThreeMonths.append(orderDetails)
    continue
  
  
  # If there was orders for that date get orders for each hour
  for hour in hours:
    ordersAmountForHour = len(getOrdersForHour(hour, ordersForDate))
    # As each hour only contains XX:XX, it doesn't have a date.
    # Combine the current hour iteration with the current date iteration 
    hour = datetime.combine(date, datetime.time(hour))
    if ordersAmountForHour == 0:
      info = {
        "hour": hour,
        "amount": 0
      }
      orderDetails["orders"].append(info) 
    else:
      info = {
        "hour": hour,
        "amount": ordersAmountForHour
      }
      orderDetails["orders"].append(info)
  orderDetailsForThreeMonths.append(orderDetails)
      

# Get ready to write to .csv file
output = QOutput("previous_three_months", ["timestamp", "orders"])

# Write all data to .csv
for date in orderDetailsForThreeMonths:
  for order in date['orders']:
    output.write([order["hour"], order["amount"]])


output.close()

