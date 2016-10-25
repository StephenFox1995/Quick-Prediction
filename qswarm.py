from nupic.swarming import permutations_runner
import os
import pprint



class QSwarm(object):
  
  # Name of the directory for the swarm data.
  SWARM_WORK_DIR_NAME = "swarm"
  INIT_FILE_NAME = "__init__.py"

  def __init__(self, swarmDescription):
    """
      Initiliases a new instance.

      @param csvFile: (string) The csv file to read the data from, which is used to generate the swarm data.
      @param swarmDescription: (string) A description of the swarm.
    """
    self._swarmDescription = swarmDescription

  
  def start(self, name="unnamed"):
    """
    Starts a new swarm.

    @param name: (string) The name to call the swarm.
    """
    self._SWARM_NAME = name
    self.__swarm()

    
  def __writeModelParams(self, modelParams):
    swarmModelParamsDir= os.path.join(QSwarm.SWARM_WORK_DIR_NAME, self._SWARM_NAME + "_model_params") 
    swarmModelParamsPyFile = self._SWARM_NAME + "_model_params.py"
    
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
    return paramsOutPath


  def __swarm(self, name, inputFile):
    swarmWorkDir = os.path.abspath(QSwarm.SWARM_WORK_DIR_NAME)
    # Create directory for the swarm details
    if not os.path.exists(swarmWorkDir):
      os.mkdir(swarmWorkDir)
    modelParams = modelParams(swarmWorkDir, SWARM_DESCRIPTION)
    writeModelParams(modelParams)
  

  def __createSwarmWorkDir(self):
    swarmWorkDir = os.path.abspath(QSwarm.SWARM_WORK_DIR_NAME)
    if not os.path.exists(swarmWorkDir): 
      os.mkdir(swarmWorkDir)
    return swarmWorkDir
  
  
  def __swarm(self):
    # Create directory for swarm details
    swarmWorkDir = self.__createSwarmWorkDir()
    modelParams = permutations_runner.runWithConfig(
        self._swarmDescription,
        {"maxWorkers": 2, "overwrite": True},
        outputLabel=self._SWARM_NAME,
        outDir=swarmWorkDir,
        permWorkDir=swarmWorkDir
    )
    # Write the model parameters to swarm directory.
    self.__writeModelParams(modelParams)

