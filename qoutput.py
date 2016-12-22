import csv
import os

# Util class for managing file and directory functionality.
class QOutput(object):
  def __init__(self):
    pass

  def __init__(self, file, headers):
    self.filename = file
    self.headers = headers
    self.lineCount = 0
    
    self.filename = "%s_out.csv" % self.filename
    self.outputFile = open(self.filename, 'w')
    print("Preparing to output data to %s" % (self.filename))
    # first write the headers to the file
    self.outputWriter = csv.writer(self.outputFile)
    self.outputWriter.writerows(headers)

  def write(self, row):
    self.outputWriter.writerow(row)
    self.lineCount += 1

  def close(self):
    self.outputFile.close()
    print("Done, Wrote %i data lines to %s" % (self.lineCount, self.filename))
  

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

    


  
  

  


    