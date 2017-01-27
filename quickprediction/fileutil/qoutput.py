import csv
import os

# Util class for managing file and directory functionality.
class QOutput(object):

  def __init__(self, filename):
    self._filename = filename
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
  def dirForBusiness(rootDir, businessID, make=False):
    """
    Create a new root directory for a business for prediction data
    if it does not already exist.
    @param rootDir:(string) The directory to check if the businesses directory exists.
    @param businessID:(string) The businessID of the business.
    @param make:(bool) Make the directory if it does not exists.
    @returns The path to the busineses root directory as a string if it was created or exists.
             If a directory doesn't exist and make=false then None will be returned.
    """
    # Get current location.
    businessDir = "%s/%s" % (rootDir, businessID)
    if not os.path.exists(businessDir) and make is True:
      os.makedirs(businessDir)
      return businessDir
    elif os.path.exists(businessDir):
      return businessDir
    else:
      return None
