import os
import random
from objects import HammerObject
from parts import BreadPart, ConvexPart, SquarePart, RoundPart, TrianglePart
import sys
import constants
import lib

class TObject(HammerObject):
    def __init__(self, parts=[], tilt_prob=0.7, max_tilt=20):
        super(TObject, self).__init__(parts, tilt_prob, max_tilt)

    def generate_urdf(self, path):
        head, handle = self.write_objs(path)
        with open('templates/mesh_template') as f:
            mesh_template = f.read()
        with open('templates/joint_template') as f:
            joint_template = f.read()
        with open('templates/template.urdf') as f:
            urdf_template = f.read()
        mesh_templates = ''
        if random.uniform(0,1) < self.tilt_prob:
            roll = 90 + random.uniform(-self.max_tilt, self.max_tilt)
            pitch = random.uniform(-self.max_tilt, self.max_tilt)
        else:
            roll = 0
            pitch = 0

        head_com = lib.get_com(head.fn)
        x, y, z = 0, 0, 0
        head_com = lib.transform_point(head_com, roll, pitch, 0, x, y, z)
        head_mass = random.uniform(*self.HEAD_MASS)
        mesh_templates += mesh_template.format(name='head',
                                               lat_fric=constants.lat_fric,
                                               roll_spin_fric=constants.roll_spin_fric,
                                               roll=roll,
                                               pitch=pitch,
                                               yaw=0,
                                               cx=head_com[0],
                                               cy=head_com[1],
                                               cz=head_com[2],
                                               x=x,
                                               y=y,
                                               z=z,
                                               mass=head_mass,
                                               filename=head.fn,
                                               red=self.COLOR[0],
                                               blue=self.COLOR[1],
                                               green=self.COLOR[2])
        handle_com = lib.get_com(head.fn)
        handle_mass = random.uniform(*self.HANDLE_MASS)
        roll, pitch, yaw = 0, 0, 0
        x, y, z = 0, 0, -handle.depth / 2
        mesh_templates += mesh_template.format(name='handle',
                                               lat_fric=constants.lat_fric,
                                               roll_spin_fric=constants.roll_spin_fric,
                                               roll=roll,
                                               pitch=pitch,
                                               yaw=0,
                                               cx=handle_com[0],
                                               cy=handle_com[1],
                                               cz=handle_com[2],
                                               x=x,
                                               y=y,
                                               z=z,
                                               mass=handle_mass,
                                               filename=handle.fn,
                                               red=self.COLOR[0],
                                               blue=self.COLOR[1],
                                               green=self.COLOR[2])
        joint_template = joint_template.format(parent_name='head',
                                               child_name='handle')
        urdf = urdf_template.format(body_name='T_hammer', links=mesh_templates, joints=joint_template)
        with open(path, 'w') as f:
            f.write(urdf)

