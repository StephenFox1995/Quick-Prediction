def connString(uri, port, database, user=None, password=None):
  if user != None and password != None:
    return "mongodb://%s:%s@%s:%s/%s" % (user, password, uri, port, database)
  else:
    return "mongodb://%s:%s/%s" % (uri, port, database)
