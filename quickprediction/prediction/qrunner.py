import csv
from nupic.frameworks.opf.modelfactory import ModelFactory
from quickprediction.utils.qoutput import QOutput
import quickprediction.prediction.swarmtype as swarmtype

class QRunner(object):

  def __init__(self):
    self.model = None


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


  def runModel(self, runName, inPath, swarmType, outDir, skiprows, func):
    """
    Runs the model.
    @param runName: (string) The name of the runName
    @param model: () The model object.
    @param inPath: (string) The file to read and write the predictions to.
    @param swarmType: () The type of swarm to run.
    @param outDir: (string) The directory to write the results of the run to.
    @param func: (function) A function thats is called on each iteration of the
      of the csv rows. It passes the row from the current iteration.
      The function should return a JSON object with the fields to run with the NuPIC model.
      The function signature looks as follows:
        - func
          @param csvRow: (object) A csv row.
          @return json: (object) JSON object with the fields to run within NuPIC.
    @return list containing all the rows written to the .csv file.
    """
    if not callable(func):
      raise ValueError('%r func arg is not callable.' % func)

    inputFile = open(inPath, "rb")
    csvReader = csv.reader(inputFile)

    # Create output file.
    runOutputFile = "%s/%s_results.csv" % (outDir, runName)
    headers = csvReader.next()
    headers.append("prediction")

    output = QOutput(runOutputFile)
    output.writeHeader(headers)

    # Set the position to start reading the csv file.
    for _ in range(0, skiprows - 1):
      csvReader.next()

    predictionData = [] # keep reference so we can return.

    # Iterate through the csv file.
    for row in csvReader:
      json = func(row)
      result = self.model.run(json)
      prediction = result.inferences["multiStepBestPredictions"][1]

      # Get the rows from the original csv and append the prediction to it and write.
      row = []
      for value in json.itervalues():
        row.append(value)
      row.append(int(prediction))
      if swarmType == swarmtype.ORD_AMOUNT:
        predictionData.append({
          "timestamp": row[0],
          "orders": row[1],
          "prediction": prediction,
        })
        output.write(row)
      elif swarmType == swarmtype.EXPECTED_EMPLOYEES:
        predictionData.append({
          "timestamp": row[0],
          "employeesNeeded": int(row[1]),
          "prediction": prediction,
        })
        output.write(row)

    inputFile.close()
    output.close()
    return predictionData
