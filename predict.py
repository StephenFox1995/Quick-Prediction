from qoutput import QOutput
from qswarm import QSwarm
from qoutput import QOutput
import os
import consts

class Predict(object):
  def __init__ (self, businessID, swarmType):
    self._businessID = businessID
    self._swarmType = swarmType
    self._dirForBusiness = QOutput.rootDirForBusiness(self._businessID, make=True)

  def begin(self, data):
    self.__writeDataToFile(data, self._swarmType)
    self._swarmer = QSwarm(self._swarmType, self._dirForBusiness, self._businessID)
    self._swarmer.start()

  def __writeDataToFile(self, data, swarmType):
    """
    Writes the data to a .csv file before being swarmed over.
    @param date(list): The data, typically as a list.
    @param swarmType(QSwarm.SwarmType): The type of swarm being performed.
    """
    # Todo: Provide callback to handle how the data
    # for each row should be parsed.
  
    dataFile = ""
    dataDir = "%s/sources/data" % self._dirForBusiness

    # Check if data directory is created.
    if not os.path.exists(dataDir):
      os.makedirs(dataDir)

    if swarmType == QSwarm.SwarmType.OrderAmount:
      dataFile = "%s/sources/data%s" % (self._dirForBusiness, consts.ORDER_AMOUNT_FILE_NAME)

      csvOut = QOutput(dataFile)
      csvOut.writeHeader(["timestamp", "orders"])
      csvOut.writeHeader(["datetime", "int"])
      csvOut.writeHeader(["T", " "])
      for row in data:
        for order in row["orders"]:
          csvOut.write([order["hour"], order["amount"]])
      csvOut.close()
