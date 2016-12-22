import os
import pprint
from enum import Enum
from nupic.swarming import permutations_runner
import json


class QSwarm(object):
  SwarmType = Enum(["OrderAmount"])
  SWARM_WORK_DIR_NAME = "swarm" # Name of the directory for the swarm data.
  INIT_FILE_NAME = "__init__.py"

  def __init__(self, swarmType, businessDir, businessID):
    self.__swarmDescriptionObject = self.getSwarmDescObject(swarmType)
    self._businessID = businessID
    self._businessDir = businessDir
    self.__newSwarmDescription(self.__swarmDescriptionObject, businessDir)
    

  def __newSwarmDescription(self, swarmDescTemplate, businessDir):
    """
    Creates a new swarm_description file for the business if one does
    not already exist.
    @param swarmDescTemplate:(object) A JSON representation of the template to 
                                      use for the swarm_description
    @param businessDir:(string) Root directory for the business.
    """

    print("Checking if a swarm_description.json exists...")
    # Check is businessDir/sources exists    
    sourcesLocation = businessDir + "/sources"
    swarmDescriptionFile = sourcesLocation + "/swarm_description.json"
    if not os.path.exists(sourcesLocation):
      print("Creating swarm_description.json file...")
      os.makedirs(sourcesLocation)
    
    if not os.path.exists(swarmDescriptionFile):
      print("Writing params to swarm_description.json file")
      self.__swarmDescriptionObject["streamDef"]["streams"][0]["source"] = self.__streamSourceFormat(self._businessID, "data.csv")
      swarmDescJSONString = json.dumps(self.__swarmDescriptionObject, indent=2)
      # Swarm description must be assigned to a property.
      with open(swarmDescriptionFile, "w") as f:
        swarmDescription = swarmDescJSONString
        f.write(swarmDescription)
        print("Params successfully written to swarm_description.json file")
    else:
      print("swarm_description.json file already exists")
      with open(swarmDescriptionFile, 'r') as f:
        swarmDescription = f.read()
        self._swarmDescriptionObject = json.loads(swarmDescription)


  def __streamSourceFormat(self, businessID, sourceFilename):
    # Example format: "file://sources/orders.csv",
    return "file://" + businessID + "/sources/" + sourceFilename


  def start(self, name="unnamed"):
    """
    Starts a new swarm.
    @param swarmDir: (string) The directory for the swarm data.
    @param name: (string) The name to call the swarm.
    """
    self.SWARM_NAME = name
    self.__swarm()


  def __writeModelParams(self, modelParams):
    """
    Writes the model_params to directory.
    @param modelParams: (dict) Model Parameters generated from swarm.
    """
    swarmModelParamsDir = os.path.join(QSwarm.SWARM_WORK_DIR_NAME, self.SWARM_NAME + "_model_params") 
    swarmModelParamsPyFile = self.SWARM_NAME + "_model_params.py"
    
    outDir = os.path.join(os.getcwd(), swarmModelParamsDir)
    if not os.path.isdir(outDir):
      os.mkdir(outDir)
    # Create the /stream/__init__.py file
    open(os.path.join(outDir, QSwarm.INIT_FILE_NAME), 'a').close()

    paramsOutPath = os.path.join(outDir, swarmModelParamsPyFile)

    # Write to model_params.py file.
    pp = pprint.PrettyPrinter(indent=2)
    with open(paramsOutPath, "wb") as outFile:
        modelParamsString = pp.pformat(modelParams)
        outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)
  

  def __createSwarmWorkDir(self):
    """
    Creates the swarm/ directory, which stores all generated files from the swarm
    """
    swarmWorkDir = os.path.abspath(QSwarm.SWARM_WORK_DIR_NAME)
    if not os.path.exists(swarmWorkDir): 
      os.mkdir(swarmWorkDir)
      # Create __init__.py
      open(os.path.join(swarmWorkDir, QSwarm.INIT_FILE_NAME), 'a').close()
    return swarmWorkDir
  
  
  def __swarm(self):
    """
    Starts a swarm and writes a generated files to swarm/ directory for the business.
    """
    # Create directory for swarm details
    swarmWorkDir = self.__createSwarmWorkDir()
    modelParams = permutations_runner.runWithConfig(
        self._swarmDescriptionObject,
        {"maxWorkers": 2, "overwrite": True},
        outputLabel=self.SWARM_NAME,
        outDir=swarmWorkDir,
        permWorkDir=swarmWorkDir
    )
    # Write the model parameters to swarm directory.
    self.__writeModelParams(modelParams)
  
  
  
  def getSwarmDescObject(self, swarmType):
    # Get the swarm desc template for appropriate swarm.
    currentDir = os.path.dirname(os.path.realpath(__file__))
    swarmDescTemplate = currentDir + "/swarm_desc_templates"
    if swarmType == QSwarm.SwarmType.OrderAmount:
      if swarmType == QSwarm.SwarmType.OrderAmount:
        swarmDescTemplate += "/order_amount_template.json"
        with open(swarmDescTemplate) as swarmDesc:
          data = json.load(swarmDesc)
          return data
