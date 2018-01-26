import os
import random
import glob
import numpy as np
from heads import Head
from lib import read_mesh, write_mesh


class ConvexHead(Head):
    def __init__(self,
                 min_radius=2e-2,
                 max_radius=5e-2,
                 min_length=8e-2,
                 max_length=15e-2,
                 z_offset=0,
                 mesh_glob='/cvgl2/u/virajm/robovat_grasp/data/simulation/tools/mpi-grasp/*/*.obj'): # NOQA
        self.paths = [os.path.abspath(path) for path in glob.glob(mesh_glob)
                      if 'vhacd' in path]
        super(ConvexHead, self).__init__(max_radius, min_radius, max_length,
                                         min_length, 0, z_offset, False, False)

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
        if np.max(diffs) > self.max_length:
            vertices *= (self.max_length / np.max(diffs))
        elif np.max(diffs) < self.min_length:
            vertices *= (self.min_length / np.max(diffs))
        # make sure x is the most variant axis and z is least(hack)
        vertices = vertices[:, np.argsort(diffs)[::-1]]

        # make sure minimum z coordinate is -0.1
        vertices[:, 2] -= min_coordinates[np.argsort(diffs)[0]] + 0.01

        write_mesh(fn, vertices, faces)


