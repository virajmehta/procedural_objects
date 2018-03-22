import os
import random
from objects import HammerObject
from parts import BreadPart, ConvexPart, SquarePart, RoundPart, TrianglePart
import sys
import constants
import lib
from ipdb import set_trace as db

class TObject(HammerObject):
    def __init__(self, parts=[], tilt_prob=0.7, max_tilt=20):
        super(TObject, self).__init__(parts, tilt_prob, max_tilt)

    def generate_urdf(self, path):
        head, handle = self.write_objs(path)
        mesh_templates = ''
        if random.uniform(0,1) < self.tilt_prob:
            roll = 90 + random.uniform(-self.max_tilt, self.max_tilt)
            pitch = random.uniform(-self.max_tilt, self.max_tilt)
        else:
            roll = 90
            pitch = 0

        head_com = lib.get_com(head.fn)
        x, y, z = 0, 0, 0
        head_com = lib.transform_point(head_com, roll, pitch, 0, x, y, z)
        head_mass = random.uniform(*self.HEAD_MASS)
        mesh_templates += self.get_link(name='head', mass=head_mass,
                filename=head.fn, roll=roll, pitch=pitch, cx=head_com[0],
                cy=head_com[1], cz=head_com[2])
        handle_com = lib.get_com(handle.fn)
        handle_mass = random.uniform(*self.HANDLE_MASS)
        roll, pitch, yaw = 0, 0, 0
        x, y, z = 0, 0, -handle.depth / 2
        mesh_templates += self.get_link(name='handle', mass=handle_mass,
                filename=handle.fn, cx=handle_com[0], cy=handle_com[1],
                cz=handle_com[2])
        joint = self.get_joint(parent_name='head', child_name='handle')
        urdf = self.get_urdf(body_name='T_hammer', links=mesh_templates,
                joints=joint)
        with open(path, 'w') as f:
            f.write(urdf)

