import os
import random
import glob
import numpy as np
from handles import Handle
from lib import read_mesh, write_mesh


class ConvexHandle(Handle):
    def __init__(self,
                 min_radius=2e-2,
                 max_radius=4e-2,
                 min_length=12e-2,
                 max_length=28e-2,
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
        min_coordinates = np.min(vertices, axis=0)
        max_coordinates = np.max(vertices, axis=0)
        vertices -= (min_coordinates + max_coordinates) / 2
        diffs = max_coordinates - min_coordinates

        # make sure z is the most variant axis and x is least(hack)
        vertices = vertices[:, np.argsort(diffs)]

        # scale to make sure the length is in bounds
        z_diff = np.max(vertices[:, 2]) - np.min(vertices[:, 2])
        vertices[:, 2] *= (random.uniform(self.min_length, self.max_length) / z_diff)

        # make sure it is as thick as it should be 
        x_diff = np.max(vertices[:, 0]) - np.min(vertices[:, 0])
        vertices[:, 0] *= (random.uniform(self.min_radius, self.max_radius) / x_diff)
        y_diff = np.max(vertices[:, 1]) - np.min(vertices[:,1])
        vertices[:, 1] *= (random.uniform(self.min_radius, self.max_radius) / y_diff)


        # make sure maximum z coordinate is 0.1
        vertices[:, 2] -= np.max(vertices[:, 2])
        vertices[:, 2] += 0.01
        
        write_mesh(fn, vertices, faces)


