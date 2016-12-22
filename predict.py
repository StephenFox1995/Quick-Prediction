from qoutput import QOutput

class Predict(object):
  def __init__ (self, businessID):
    QOutput.dirForBusiness(businessID, make=True)
  
  

