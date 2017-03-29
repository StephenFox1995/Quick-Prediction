import radar
import argparse
import random
from pprint import pprint
from datetime import timedelta, datetime
from quickprediction.dbs.orderdb import OrderDB
from quickprediction.config.configuration import Configuration
from bson.objectid import ObjectId


config = Configuration()
dbDetails = config.read([Configuration.DATABASES])[0][0]

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-s", "--start", help="The start date format: dd-mm-yyyy", dest="start")
  parser.add_argument("-e", "--end", help="The end date format: dd-mm-yyyy", dest="end")
  parser.add_argument("-n", "--number", help="The number of records", dest="number")
  args = parser.parse_args()
  print(args)
  start = datetime.strptime(args.start, "%d%m%Y")
  end = datetime.strptime(args.end, "%d%m%Y")
  records = int(args.number)
  # Connect to the database
  orderDB = OrderDB(
    dbDetails["uri"],
    dbDetails["port"],
    dbDetails["database"],
    dbDetails["username"],
    dbDetails["password"])
  orderDB.connect()

  bulkop = orderDB.bulkop

  for i in range(0, records):
    order = {
      "businessID": ObjectId("58876b6905733be97fb526ad"),
      "userID" : ObjectId("58876b4d05733be97fb526ac"),
	    "products": [],
      "status" : "processed",
      "coordinates" : {
        "lat" : 53.3734815649692,
        "lng" : -6.31733807775909
      },
      "release" : "",
      "deadline" : "",
      "finish" : "",
      "createdAt" : "",
      "travelMode": "walking",
      "processing": random.randrange(0, 700),
      "cost": 3.45
    }
    date = radar.random_datetime(start='2016-11-01', stop=datetime.now())
    order["deadline"] = date
    order["finish"] = date
    order["release"] = date - timedelta(minutes=5)
    order["createdAt"] = date - timedelta(minutes=10)

    print("created at: %s" % order["createdAt"])
    print("release at: %s" % order["release"])
    print("deadline at: %s\n" % order["deadline"])
    bulkop.insert(order)
  result = bulkop.execute()
  pprint(result)
