import os
import random
import glob
import numpy as np
from parts import Part
from lib import read_mesh, write_mesh


class ConvexPart(Part):
    def __init__(self,
                 min_length,
                 max_length,
                 min_width,
                 max_width,
                 min_depth,
                 max_depth,
                 mesh_glob='/cvgl2/u/virajm/robovat_grasp/data/simulation/tools/mpi-grasp/*/*.obj'): # NOQA
        super(ConvexPart, self).__init__(min_length, max_length, min_width, max_width,
                                          min_depth, max_depth)
        self.paths = [os.path.abspath(path) for path in glob.glob(mesh_glob)
                      if 'vhacd' in path]

    def get_random_scad(self):
        return ''

    def write_obj(self, fn):
        path = random.choice(self.paths)
        vertices, faces, _ = read_mesh(path)
        min_coordinates = np.min(vertices, axis=0)
        max_coordinates = np.max(vertices, axis=0)
        vertices -= (min_coordinates + max_coordinates) / 2
        diffs = max_coordinates - min_coordinates

        # make sure z is the most variant axis and x is least(hack)
        vertices = vertices[:, np.argsort(diffs)]

        self.depth = random.uniform(self.min_depth, self.max_depth)
        self.width = random.uniform(self.min_width, self.max_width)
        self.length = random.uniform(self.min_length, self.max_length)

        # scale to make sure the length is in bounds
        z_diff = np.max(vertices[:, 2]) - np.min(vertices[:, 2])
        vertices[:, 2] *= self.depth / z_diff

        # make sure it is as thick as it should be 
        x_diff = np.max(vertices[:, 0]) - np.min(vertices[:, 0])
        vertices[:, 0] *= self.length / z_diff
        y_diff = np.max(vertices[:, 1]) - np.min(vertices[:,1])
        vertices[:, 1] *= self.width / z_diff

        write_mesh(fn, vertices, faces)


