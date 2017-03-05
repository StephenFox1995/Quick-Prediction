import os
import pprint
import json
from nupic.swarming import permutations_runner
from quickprediction.utils import fileutil
from . import swarmtype


class QSwarm(object):
  def __init__(self, swarmType, businessDir, businessID):
    self._swarmDescriptionObject = self.__getSwarmDescObject(swarmType)
    self._businessID = businessID
    self._businessDir = businessDir
    self._swarmType = swarmType
    self.__newSwarmDescription(self._swarmDescriptionObject, businessDir)
    self._swarmName = None

  def __newSwarmDescription(self, swarmDescTemplate, businessDir):
    """
    Creates a new swarm_description file for the business if one does
    not already exist.
    @param swarmDescObject:(object) A JSON representation of the template to
                                      use for the swarm_description
    @param businessDir:(string) Root directory for the business.
    """
    print("Checking if a swarm_description.json exists...")
    # Check is businessDir/sources exists
    sourcesDir = os.path.join(businessDir, "sources")
    if self._swarmType == swarmtype.ORD_AMOUNT:
      self._swarmDescriptionFile = os.path.join(sourcesDir, 'orderamount', 'swarm_description.json')
    elif self._swarmType == swarmtype.EXPECTED_EMPLOYEES:
      self._swarmDescriptionFile = os.path.join(sourcesDir, 'employeesneeded', 'swarm_description.json')
    if not os.path.exists(sourcesDir):
      print("Creating swarm directory...")
      os.makedirs(sourcesDir)

    if not os.path.exists(self._swarmDescriptionFile):
      print("Writing params to swarm_description.json file")
      swarmDescTemplate["streamDef"]["streams"][0]["source"] = self.__streamSourceFormat()
      swarmDescJSONString = json.dumps(self._swarmDescriptionObject, indent=2)

      # Swarm description must be assigned to a property.
      with open(self._swarmDescriptionFile, "w") as f:
        swarmDescription = swarmDescJSONString
        f.write(swarmDescription)
        print("Params successfully written to swarm_description.json file")

    else:
      print("swarm_description.json file already exists")
      with open(self._swarmDescriptionFile, 'r') as f:
        swarmDescription = f.read()
        self._swarmDescriptionObject = json.loads(swarmDescription)


  def __streamSourceFormat(self):
    if self._swarmType == swarmtype.ORD_AMOUNT:
      return fileutil.swarmDescPath(self._businessDir, self._swarmType, fileutil.ORDER_AMOUNT_FILE_NAME)
    else:
      return fileutil.swarmDescPath(self._businessDir, self._swarmType, fileutil.EXPECTED_EMPLOYEES_FILE_NAME)


  def start(self, name="unnamed"):
    """
      Starts a new swarm.
      @param swarmDir: (string) The directory for the swarm data.
      @param name: (string) The name to call the swarm.
      @param (object) The model parameters generated from the swarm.
    """
    self._swarmName = name
    return self.__swarm()


  def __writeModelParams(self, modelParams):
    """
      Writes the model_params to directory.
      @param modelParams: (dict) Model Parameters generated from swarm.
    """
    swarmModelParamsFile = self._swarmName + "_model_params.py"
    swarmModelParamsDir = ""
    if self._swarmType == swarmtype.ORD_AMOUNT:
      swarmModelParamsDir = os.path.join(
        self._businessDir,
        fileutil.SWARM_DIR_NAME,
        "orderamount",
        swarmModelParamsFile
      )
    elif self._swarmType == swarmtype.EXPECTED_EMPLOYEES:
      swarmModelParamsDir = os.path.join(
        self._businessDir,
        fileutil.SWARM_DIR_NAME,
        "employeesneeded",
        swarmModelParamsFile
      )

    if not os.path.isdir(swarmModelParamsDir):
      os.makedirs(swarmModelParamsDir)
    # Create the /stream/__init__.py file
    open(os.path.join(swarmModelParamsDir, fileutil.INIT_FILE_NAME), 'a').close()
    paramsOutPath = os.path.join(swarmModelParamsDir, swarmModelParamsFile)

    # Write to model_params.py file.
    with open(paramsOutPath, "wb") as outFile:
      pp = pprint.PrettyPrinter(indent=2)
      modelParamsString = pp.pformat(modelParams)
      outFile.write("MODEL_PARAMS = \\\n%s" % modelParamsString)



  def __createSwarmWorkDir(self):
    """
    Creates the swarm/ directory, which stores all generated files from the swarm
    """
    baseDir = os.path.join(self._businessDir, fileutil.SWARM_DIR_NAME)
    if not os.path.exists(baseDir):
      os.mkdir(baseDir)
    swarmWorkDir = {}
    if self._swarmType == swarmtype.ORD_AMOUNT:
      swarmWorkDir = os.path.join(baseDir, "orderamount")
    elif self._swarmType == swarmtype.EXPECTED_EMPLOYEES:
      swarmWorkDir = os.path.join(baseDir, "employeesneeded")
    if not os.path.exists(swarmWorkDir):
      os.mkdir(swarmWorkDir)
      # Create __init__.py
      open(os.path.join(swarmWorkDir, fileutil.INIT_FILE_NAME), 'a').close()
    return swarmWorkDir


  def __swarm(self):
    """
    Starts a swarm and writes a generated files to swarm/ directory for the business.
    @return modelParam:(object) Models Parameters object.
    """
    # Create directory for swarm details
    swarmWorkDir = self.__createSwarmWorkDir()
    modelParams = permutations_runner.runWithConfig(
        self._swarmDescriptionObject,
        {"maxWorkers": 2, "overwrite": True},
        outputLabel=self._swarmName,
        outDir=swarmWorkDir,
        permWorkDir=swarmWorkDir
    )
    # Write the model parameters to swarm directory.
    self.__writeModelParams(modelParams)
    return modelParams


  def __getSwarmDescObject(self, swarmType):
    # Get the swarm desc Object for appropriate swarm.
    currentDir = os.path.dirname(os.path.abspath(__file__))
    swarmDescDir = os.path.join(currentDir, "swarm_desc_templates")
    swarmDescFile = {}
    if swarmType == swarmtype.ORD_AMOUNT:
      swarmDescFile = os.path.join(swarmDescDir, "order_amount_template.json")
    elif swarmType == swarmtype.EXPECTED_EMPLOYEES:
      swarmDescFile = os.path.join(swarmDescDir, "expected_employees_template.json")
    with open(swarmDescFile) as swarmDesc:
      data = json.load(swarmDesc)
      return data
