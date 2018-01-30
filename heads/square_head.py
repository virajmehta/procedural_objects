import random
from math import sqrt
from heads import Head


class SquareHead(Head):
    def __init__(self,
                 min_radius=2e-2,
                 max_radius=3.5e-2,
                 min_length=10e-2,
                 max_length=20e-2,
                 max_tilt=20,
                 z_offset=0,
                 no_tilt_prob=0.2,
                 is_L=False,
                 is_X=False):
        super(SquareHead, self).__init__(min_radius, max_radius, min_length,
                                         max_length, max_tilt, z_offset,
                                         is_L, is_X)
        self.scad = ' length = {0}; girth = {1}; translate([{3},0,{4}]){{rotate(a=[{5},{2},0]){{translate([length / -2, girth / -2, 0.]) {{ cube([length, girth, girth]); }} }} }};'  # NOQA
        self.min_square_side_length = sqrt(2) * min_radius
        self.max_square_side_length = sqrt(2) * max_radius
        self.no_tilt_prob = no_tilt_prob

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        square_side_length = random.uniform(self.min_square_side_length,
                                            self.max_square_side_length)
        tilt = 0
        roll = 0
        z_offset = 0
        x_offset = 0
        if random.random() > self.no_tilt_prob:
            tilt = random.uniform(-self.max_tilt, self.max_tilt)
            roll = random.uniform(-self.max_tilt, self.max_tilt)
        if self.is_L:
            x_offset = (length / 2) - 3e-2
        if self.is_X:
            z_offset = random.uniform(-15e-2, 0)
        return self.scad.format(length, square_side_length, tilt, x_offset,
                                z_offset, roll)
