from qoutput import QOutput
from qswarm import QSwarm
from qoutput import QOutput
from qrunner import QRunner
import swarmtype
import os
import fileutil
import rowextract

class Predict(object):

  def __init__ (self, businessID, swarmType, rootDir):
    self._businessID = businessID
    self._swarmType = swarmType
    self._rootDir = rootDir
    self._dirForBusiness = QOutput.dirForBusiness(rootDir, self._businessID, make=True)

  def begin(self, data):
    """
    Begins the process of swarming and then running the model.
    @param data: (list) The list of data to perform predictions on.
    """
    self.__writeDataToFile(data, self._swarmType)
    self._swarmer = QSwarm(self._swarmType, self._dirForBusiness, self._businessID)
    self._modelParams = self._swarmer.start()
    self._runner = QRunner()
    if self._swarmType == swarmtype.ORD_AMOUNT:
      self._runner.createModel(self._modelParams, "orders")
      self._runner.runModel(
        "orderAmountRun", 
        self._dataFile, 
        self._dirForBusiness,
        3, 
        rowextract.orderAmountRows)


  def __writeDataToFile(self, data, swarmType):
    """
    Writes the data to a .csv file before being swarmed over.
    @param date(list): The data, typically as a list.
    @param swarmType(string): The type of swarm being performed.
    """
    # Todo: Provide callback to handle how the data
    # for each row should be parsed.
  
    dataDir = "%s/sources/data" % self._dirForBusiness

    # Check if data directory is created.
    if not os.path.exists(dataDir):
      os.makedirs(dataDir)

    if swarmType == swarmtype.ORD_AMOUNT:
      self._dataFile = "%s/sources/data%s" % (self._dirForBusiness, fileutil.ORDER_AMOUNT_FILE_NAME)

      csvOut = QOutput(self._dataFile)
      csvOut.writeHeader(["timestamp", "orders"])
      csvOut.writeHeader(["datetime", "int"])
      csvOut.writeHeader(["T", " "])
      for row in data:
        for order in row["orders"]:
          csvOut.write([order["hour"], order["amount"]])
      csvOut.close()
  
 