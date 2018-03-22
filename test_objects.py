import sys
import os
import pybullet
from ipdb import set_trace as db


def main(objects):
    client = pybullet.connect(pybullet.GUI)
    for obj in objects:
        pybullet.resetSimulation(client)
        pybullet.loadURDF(obj)
        input('Enter to continue')



if __name__ == '__main__':
    main(sys.argv[1:])
