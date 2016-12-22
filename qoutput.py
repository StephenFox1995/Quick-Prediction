import csv
import os

# Util class for managing file and directory functionality.
class QOutput(object):

  def __init__(self, file):
    self._filename = file
    self._headers = []
    self._lineCount = 0
    self._outputFile = open(self._filename, 'w+')
    self._headersWritten = False
    self._outputWriter = csv.writer(self._outputFile)
    print("Preparing to output data to %s" % (self._filename))
    
    
  def writeHeader(self, header):
    self._outputWriter.writerow(header)

  def write(self, row):
    self._outputWriter.writerow(row)
    self._lineCount += 1

  def close(self):
    self._outputFile.close()
    print("Done, Wrote %i data lines to %s" % (self._lineCount, self._filename))
  
  @staticmethod
  def rootDirForBusiness(id, make=False):
    """
    Create a new root directory for a business for prediction data
    if it does not already exist.
    """
    # Get current location.
    dirPath = os.path.dirname(os.path.realpath(__file__))
    businessDir = dirPath + "/" + id
    if not os.path.exists(businessDir) and make == True:
      os.makedirs(businessDir)
    return businessDir

    


  
  

  


    