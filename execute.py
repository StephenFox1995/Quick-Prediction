from qswarm import QSwarm
from sources.swarm_description import SWARM_DESCRIPTION


if __name__ == "__main__":
    qswarm = QSwarm(SWARM_DESCRIPTION)
    qswarm.start("purchases_swarm")



