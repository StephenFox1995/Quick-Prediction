import radar
from datetime import timedelta, datetime
from quickprediction.dbs.orderdb import OrderDB
from quickprediction.config.configuration import Configuration
from bson.objectid import ObjectId


config = Configuration()
dbDetails = config.read([Configuration.DATABASES])[0][0]

if __name__ == "__main__":
  # Connect to the database
  orderDB = OrderDB(
    dbDetails["uri"],
    dbDetails["port"],
    dbDetails["database"],
    dbDetails["username"],
    dbDetails["password"]
  )
  orderDB.connect()

  for i in range(0, 10000):
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
      "processing": 0,
      "cost": 3.45
    }
    date = radar.random_datetime(start='2016-11-01', stop=datetime.now())
    order["deadline"] = date
    order["finish"] = date
    order["release"] = date - timedelta(minutes=-5)
    order["createdAt"] = date - timedelta(minutes=-10)

    print("created at: %s" % order["createdAt"])
    print("release at: %s" % order["release"])
    print("deadline at: %s\n" % order["deadline"])
    orderDB.insert(order)
