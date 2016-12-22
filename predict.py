from qoutput import QOutput
from qswarm import QSwarm

class Predict(object):
  def __init__ (self, businessID, swarmType):
    self._businessID = businessID
    self._dirForBusiness = QOutput.rootDirForBusiness(businessID, make=True)
    self._swarmer = QSwarm(swarmType, self._dirForBusiness, businessID)

  def begin(self, data):
    self._swarmer.start()