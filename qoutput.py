import csv

class QOutput(object):
  
  def __init__(self, file, headers):
    self.filename = file
    self.headers = headers
    self.lineCount = 0
    
    self.filename = "%s_out.csv" % self.filename
    self.outputFile = open(self.filename, 'w')
    print("Preparing to output data to %s" % (self.filename))
    # first write the headers to the file
    self.outputWriter = csv.writer(self.outputFile)
    self.outputWriter.writerow(headers)


  def write(self, row):
    self.outputWriter.writerow(row)
    self.lineCount += 1

  
  def close(self):
    self.outputFile.close()
    print("Done, Wrote %i data lines to %s" % (self.lineCount, self.filename))
  

  


    