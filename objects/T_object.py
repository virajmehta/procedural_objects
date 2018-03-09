import os
import random
from objects import HammerObject
from parts import *
import constants

class TObject(HammerObject):

    def generate_urdf(self, path):
        head, handle = self.write_objs(path)
        with open('templates/mesh_template') as f:
            mesh_template = f.read()
        mesh_templates = ''
        if random.uniform() < self.tilt_prob:
            roll = 90 + random.uniform(-self.max_tilt, self.max_tilt)
            pitch = random.uniform(-self.max_tilt, self.max_tilt)

        head_com = get_com(head.fn)
        x, y, z = 0, 0, 0
        head_com = transform_point(head_com, roll, pitch, 0, x, y, z)
        mesh_templates += mesh_template.format(name='head'
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
                                               filename=head.fn)
        roll, pitch, yaw = 0, 0, 0
        x, y, z = 0, 0, -handle.depth / 2




