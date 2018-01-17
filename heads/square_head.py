import random
from math import sqrt
from heads import Head

class SquareHead(Head):
    def __init__(self,
                 min_radius=2e-2,
                 max_radius=5e-2,
                 min_length=10e-2,
                 max_length=20e-2,
                 z_offset=0):
        super(SquareHead, self).__init__(max_radius, min_radius, max_length, min_length, z_offset)
        self.scad = ' length = {0}; girth = {1}; translate([length / -2, girth / -2, 0.]) {{ cube([length, girth, girth]); }};'
        self.min_square_side_length = sqrt(2) * min_radius
        self.max_square_side_length = sqrt(2) * max_radius

    def get_random_scad(self):
       length = random.uniform(self.min_length, self.max_length)
       square_side_length = random.uniform(self.min_square_side_length, self.max_square_side_length)
       return self.scad.format(length, square_side_length)
