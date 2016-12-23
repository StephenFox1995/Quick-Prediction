from nupic.frameworks.opf.modelfactory import ModelFactory
import csv
import datetime
from qoutput import QOutput 

class QRunner(object):

  
  def createModel(self, modelParams, predictedField):
    """
    Creates a model.
    @param modelParams: () The modelParams used for running the model.
    @param predictedField: (string) The predictedField.
    """
    model = ModelFactory.create(modelParams)
    model.enableInference({
      "predictedField": predictedField
    })
    self.model = model


  def runModel(self, runName, inPath, outDir, skiprows, closure):
    """
    Runs the model.
    @param runName: (string) The name of the runName
    @param model: () The model object.
    @param inPath: (string) The file to read and write the predictions to.
    @param outDir: (string) The directory to write the results of the run to.
    @param closure: (function) A function thats is called on each iteration of the
      of the csv rows. It passes the row from the current iteration.
      The function should return a JSON object with the fields to run with the NuPIC model.
      The function signature looks as follows:
        - closure
          @param csvRow: (object) A csv row.
          @return json: (object) JSON object with the fields to run within NuPIC.
    """
    inputFile = open(inPath, "rb")
    csvReader = csv.reader(inputFile)
    
    # Create output file.
    runOutputFile = "%s/%s_results.csv" % (outDir, runName)
    headers = csvReader.next()
    headers.append("prediction")

    output = QOutput(runOutputFile)
    output.writeHeader(headers)
    
    # Set the position to start reading the csv file.
    for i in range(0, skiprows - 1):
      csvReader.next()

    # Iterate through the csv file.
    for row in csvReader:
      json = closure(row)
      result = self.model.run(json)
      prediction = result.inferences["multiStepBestPredictions"][1]
      
      # Get the rows from the original csv and append the prediction to it and write.
      row = []
      for value in json.itervalues():
        row.append(value)
      row.append(prediction)
      output.write(row)

    inputFile.close()
    output.close()
    
    

    


    
