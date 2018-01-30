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
                 max_tilt=20,
                 no_tilt_prob=0.2,
                 is_L=False,
                 is_X=False,
                 z_offset=0,
                 mesh_glob='/cvgl2/u/virajm/robovat_grasp/data/simulation/tools/mpi-grasp/*/*.obj'): # NOQA
        self.paths = [os.path.abspath(path) for path in glob.glob(mesh_glob)
                      if 'vhacd' in path]
        self.no_tilt_prob = no_tilt_prob
        super(ConvexHead, self).__init__(min_radius, max_radius, min_length,
                                         max_length, 0, z_offset, is_L, is_X)

    def get_random_scad(self):
        return ''

    def write_obj(self, fn):
        path = random.choice(self.paths)
        vertices, faces, _ = read_mesh(path)
        min_coordinates = np.min(vertices, axis=0)
        max_coordinates = np.max(vertices, axis=0)
        vertices -= (min_coordinates + max_coordinates) / 2
        diffs = max_coordinates - min_coordinates
        
        # make sure x is the most variant axis and z is least(hack)
        vertices = vertices[:, np.argsort(diffs)[::-1]]

        # scale to make sure the length is in bounds
        x_diff = np.max(vertices[:, 0]) - np.min(vertices[:, 0])
        vertices[:, 0] *= (random.uniform(self.min_length, self.max_length) / x_diff)

        # make sure it is as thick as it should be 
        y_diff = np.max(vertices[:, 1]) - np.min(vertices[:,1])
        vertices[:, 1] *= (random.uniform(self.min_radius, self.max_radius) / y_diff)
        z_diff = np.max(vertices[:, 2]) - np.min(vertices[:,2])
        vertices[:, 2] *= (random.uniform(self.min_radius, self.max_radius) / z_diff)

        # make sure minimum z coordinate is -0.1
        vertices[:, 2] -= np.min(vertices[:, 2]) + 0.01

        if self.is_X:
            vertices[:, 2] += random.uniform(-15e-2, 0)
        if self.is_L:
            if random.choice([True, False]):
                vertices[:, 0] -= np.min(vertices[:, 0]) + 4e-2
            else:
                vertices[:, 0] -= np.max(vertices[:, 0]) - 4e-2
            vertices[:, 2] -= np.max(vertices[:, 2])
        
        if random.random() > self.no_tilt_prob:
            tilt = random.uniform(-self.max_tilt, self.max_tilt)
            tilt = np.deg2rad(tilt)
            tilt_matrix = np.array([[np.cos(tilt), 0, np.sin(tilt)],
                                    [0, 1, 0],
                                    [-np.sin(tilt), 0, np.cos(tilt)]])
            vertices = np.dot(tilt_matrix, vertices.T).T
        if random.random() > self.no_tilt_prob:
            roll = random.uniform(-self.max_tilt, self.max_tilt)
            roll = np.deg2rad(roll)
            roll_matrix = np.array([[np.cos(roll), 0, np.sin(roll)],
                                    [0, 1, 0],
                                    [-np.sin(roll), 0, np.cos(roll)]])
            vertices = np.dot(roll_matrix, vertices.T).T
        write_mesh(fn, vertices, faces)


