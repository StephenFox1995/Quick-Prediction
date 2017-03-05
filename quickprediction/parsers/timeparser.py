from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from intervaltree import IntervalTree
from quickprediction.utils.intervaltreeutil import findConflicts
from .hours import hours

__all__ = ["extractHourlyOrders", "extractHourlyConflicts"]

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



def zeroFillOrdersForFullDay(date):
  return map(lambda hour: {"hour": datetime.combine(date, datetime.time(hour)), "amount": 0}, hours)


def getTimeStampsFromMongoOrderData(orders):
  """
  Extracts the timestamp property from each order in the list.
  @param orders:(list) The list of orders.
  @return List of timestamps.
  """
  def extractTime(current):
    return current["createdAt"]
  # Get all timestamps from mongo
  return map(extractTime, orders)


def getDaysInDateRange(start, end):
  """
  Find all the dates within a given date range.
  """
  def dateRange(start, end, increment, period):
    # http://stackoverflow.com/a/10688309/2875074
    result = []
    nxt = start
    delta = relativedelta(**{period:increment})
    while nxt <= end:
      result.append(nxt)
      nxt += delta
    return result
  return dateRange(start, end, 1, 'days')


def extractHourlyOrders(orders, fromDate, toDate=datetime.today()):
  """
  Extract the hourly orders for each hour from a given date range.
  @param orders:(list) A list of orders, which contain a timestamp field.
  @param fromDate:(datetime) The beginning of the date range.
  @param toDate:(datetime) The ending datetime range.
  @return A list of the number of orders for each hour of each day in the date range.
  """
  orderTimeStamps = getTimeStampsFromMongoOrderData(orders)
  toDate = datetime.today() + timedelta(days=1)
  # Every day fromDate to toDate.
  dateRange = getDaysInDateRange(fromDate, toDate)

  orderDetailsForDateRange = []
  for date in dateRange:
    orderDetails = {
      "date": object,
      "orders": []
    }
    orderDetails["date"] = date
    # Get the orders for this date
    ordersForDate = getOrdersForDate(date, orderTimeStamps)
    # If order number is zero just fill all hours with order amount = 0
    if len(ordersForDate) == 0:
      orderDetails["orders"] = zeroFillOrdersForFullDay(date)
      orderDetailsForDateRange.append(orderDetails)
      continue

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
    orderDetailsForDateRange.append(orderDetails)
  return orderDetailsForDateRange


def workersNeeded(k, m):
  """
  Calculates the number of employees needed to deal with a conflict.
  @param k:() The number of conflicts
  @param m:() The highest number of tasks employees can service simultaneously.
  """
  # formula: k/m
  from math import ceil
  return ceil(float(k)/float(m))


def highestConflictsForHour(conflicts):
  """
    Find the highest number of conflicts for within an hour.
  """
  highest = []
  for conflict in conflicts:
    if len(conflict) > len(highest):
      highest = conflict
  return highest


def extractHourlyConflicts(orders, fromDate, toDate=datetime.today(), multitask=2):
  """
    Extracts the conflicts per hour for the date range from the orders.
  """
  def extractReleaseDeadline(order):
    return {
      "id": str(order["_id"]),
      "release": order["release"],
      "deadline": order["deadline"],
    }
  allConflicts = []
  # convert all order to tasks.
  orders = map(extractReleaseDeadline, orders)
  intervalTree = IntervalTree()
  for index, order in enumerate(orders):
    intervalTree.addi(
      begin=order["release"],
      end=order["deadline"],
      data=order["id"]
    )
  toDate = datetime.today() + timedelta(days=1)
  dateRange = getDaysInDateRange(fromDate, toDate)
  # now get conflicts for each hour
  for date in dateRange:
    conflictsForDate = {
      "date": date,
      "conflicts" : []
    }
    year = date.year
    month = date.month
    day = date.day
    for hour in range(0, 24):
      begin = datetime(year, month, day, hour, 00)
      end = datetime(year, month, day, hour, 59)
      conflicts, nonConflicts = findConflicts(intervalTree, begin, end)
      highest = highestConflictsForHour(conflicts)
      conflictsForHour = {
        "hour": begin,
        "size": len(highest),
        "employeesNeeded": workersNeeded(len(highest), multitask)
      }
      conflictsForDate["conflicts"].append(conflictsForHour)
    allConflicts.append(conflictsForDate)
  return allConflicts
