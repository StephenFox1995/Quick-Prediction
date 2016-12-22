from qoutput import QOutput
from qswarm import QSwarm

class Predict(object):
  def __init__ (self, businessID, swarmType):
    self._businessID = businessID
    self._swarmType = swarmType
    self._dirForBusiness = QOutput.rootDirForBusiness(self._businessID, make=True)

  def begin(self, data):
    self._swarmer = QSwarm(self._swarmType, self._dirForBusiness, self._businessID)
    self._swarmer.start()