import datetime
def orderAmountRows(row):
  """
  Extracts the correct information for each row, when the
  swarm type is OrderAmount.
  """
  DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
  timestamp = datetime.datetime.strptime(row[0], DATE_TIME_FORMAT)
  purchase = int(row[1])
  return {
    "timestamp": timestamp,
    "orders": purchase
  }

def employeesNeededRows(row):
  """
    Extracts the correct information for each row, when the
    swarm type is ExpectedEmployees.
  """
  DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
  timestamp = datetime.datetime.strptime(row[0], DATE_TIME_FORMAT)
  employeedNeeded = int(row[1])
  return {
    "timestamp": timestamp,
    "employeesNeeded": employeedNeeded
  }