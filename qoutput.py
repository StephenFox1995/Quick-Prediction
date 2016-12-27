import csv
import os
import fileutil

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
    @param id:(string) The id of the business.
    @param make:(bool) Make the directory if it does not exists.
    @returns The path to the busineses root directory as a string if it was created or exists.
             If a directory doesn't exist and make=false then None will be returned.
    """
    # Get current location.
    businessDir = "%s/%s" % (fileutil.ROOT_OUT_DIR, id)
    if not os.path.exists(businessDir) and make == True:
      os.makedirs(businessDir)
      return businessDir
    elif os.path.exists(businessDir):
      return businessDir
    else:
      return None
  
    


  
  

  


    