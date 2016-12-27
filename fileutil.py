import os

# The file name for orderamount swarm type. 
# All data has been generated from running the model
# will be written to this file.
ORDER_AMOUNT_FILE_NAME = "/orderAmountData.csv"

# The root directory to write all the files to during execution.
ROOT_OUT_DIR="/Users/stephenfox/Desktop/pred_test"

# The filepath to the data for a swarm
# see https://github.com/numenta/nupic/wiki/Running-Swarms
SWARM_DESC_FILE_PATH = "file://%s/sources/data%s"

def dirOK(dir):
  if not os.path.isdir(dir):
    os.makedirs(dir)
    


    
    