from qswarm import QSwarm
from swarm_description import SWARM_DESCRIPTION

CSV_FILE = "purchases_hourly.csv"

if __name__ == "__main__":
    qswarm = QSwarm(CSV_FILE, SWARM_DESCRIPTION)
    qswarm.start("purchases_swarm")



