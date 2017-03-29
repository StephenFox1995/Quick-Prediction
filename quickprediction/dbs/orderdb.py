from .database import Database


class OrderDB(Database):
  def __init__(self, uri, port, dbName, user=None, password=None):
    super(OrderDB, self).__init__(uri, port, dbName, user, password)

  def read(self, fromDate):
    """
    Get orders from the databases starting at the fromDate argument.
    @param fromDate:(datetime.datetime) The start date to get the order froms.
    """
    super(OrderDB, self).read()
    pipeline =  {"$and": [{"status": "processed"}, {"createdAt": {"$gte": fromDate}}] }
    return self._database.orders.find(pipeline).sort([("release", -1)])

  def insert(self, order):
    self._database.orders.insert(order);

  @property
  def bulkop(self):
    return self._database.orders.initialize_ordered_bulk_op()