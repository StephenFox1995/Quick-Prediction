import quickprediction.prediction.swarmtype as swarmType

# The file name for orderamount swarm type.
# All data has been generated from running the model
# will be written to this file.
ORDER_AMOUNT_FILE_NAME = "orderAmountData.csv"

EXPECTED_EMPLOYEES_FILE_NAME = "expectedEmployees.csv"

# The filepath to the data for a swarm
# see https://github.com/numenta/nupic/wiki/Running-Swarms
# SWARM_DESC_FILE_PATH = "file://%s/sources/data%s"
def swarmDescPath(directory, swarmtype, filename):
  if swarmtype == swarmType.ORD_AMOUNT:
    return "file://%s/sources/orderamount/data/%s" % (directory, filename)
  elif swarmtype == swarmType.EXPECTED_EMPLOYEES:
    return "file://%s/sources/employeesneeded/data/%s" % (directory, filename)

# Init file
INIT_FILE_NAME = "__init__.py"

# Directory name for swarm data.
SWARM_DIR_NAME = "swarm"
