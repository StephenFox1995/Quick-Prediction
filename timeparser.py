from datetime import datetime
from dateutil.relativedelta import relativedelta
from hours import hours


class TimeParser(object):

  @staticmethod
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

  @staticmethod
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

  @staticmethod
  def zeroFillOrdersForFullDay(date):
    return map(lambda hour: {"hour": datetime.combine(date, datetime.time(hour)), "amount": 0}, hours)

  @staticmethod
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


  @staticmethod
  def extractHourlyOrders(orders, fromDate, toDate=datetime.today()):
    """
    Extract the hourly orders for each hour from a given date range.
    @param orders:(list) A list of orders, which contain a timestamp field.
    @param fromDate:(datetime) The beginning of the date range.
    @param toDate:(datetime) The ending datetime range.
    @return A list of the number of orders for each hour of each day in the date range.
    """
    orderTimeStamps = TimeParser.getTimeStampsFromMongoOrderData(orders)
    # Every day fromDate to toDate.
    dateRange = TimeParser.getDaysInDateRange(fromDate, toDate)

    orderDetailsForDateRange = []
    for date in dateRange:
      orderDetails = {
        "date": object,
        "orders": []
      }
      orderDetails["date"] = date
      # Get the orders for this date
      ordersForDate = TimeParser.getOrdersForDate(date, orderTimeStamps)
      # If order number is zero just fill all hours with order amount = 0
      if len(ordersForDate) == 0:
        orderDetails["orders"] = TimeParser.zeroFillOrdersForFullDay(date)
        orderDetailsForDateRange.append(orderDetails)
        continue

      for hour in hours:
        ordersAmountForHour = len(TimeParser.getOrdersForHour(hour, ordersForDate))
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


  @staticmethod
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
