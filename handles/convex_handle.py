import os
import random
import glob
import numpy as np
from handles import Handle
from lib import read_mesh, write_mesh


class ConvexHandle(Handle):
    def __init__(self,
                 min_radius=2e-2,
                 max_radius=5e-2,
                 min_length=8e-2,
                 max_length=15e-2,
                 mesh_glob='/cvgl2/u/virajm/robovat_grasp/data/simulation/tools/mpi-grasp/*/*.obj'): # NOQA
        self.paths = [os.path.abspath(path) for path in glob.glob(mesh_glob)
                      if 'vhacd' in path]
        super(ConvexHandle, self).__init__(min_length, max_length, min_radius,
                                           max_radius)

    def get_random_scad(self):
        return ''

    def write_obj(self, fn):
        path = random.choice(self.paths)
        vertices, faces, _ = read_mesh(path)
        vertices -= np.mean(vertices, axis=0)
        min_coordinates = np.min(vertices, axis=0)
        max_coordinates = np.max(vertices, axis=0)
        diffs = max_coordinates - min_coordinates

        # scale to make sure the length is in bounds
        if np.max(diffs) > self.max_length or np.max(diffs) < self.min_length:
            vertices *= (random.uniform(self.min_length, self.max_length) /
                         np.max(diffs))
        # make sure z is the most variant axis and x is least(hack)
        vertices = vertices[:, np.argsort(diffs)]
        x_diff = np.max(vertices[:, 0]) - np.min(vertices[:, 0])

        # make sure it is at least as thick as it should be (too thick is OK)
        if x_diff < self.min_radius or x_diff > self.max_radius:
            vertices[:, :2] *= random.uniform(self.min_radius, self.max_radius)\
                                        * 2

        # make sure minimum z coordinate is -0.1
        vertices[:, 2] -= np.max(vertices[:, 2])
        write_mesh(fn, vertices, faces)


