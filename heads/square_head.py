import random
from part import Part

class SquareHead(Part):
    def __init__(self):
        self.scad = ' length = {0}; girth = {1}; translate([length / -2, girth / -2, 0.]) {{ cube([length, girth, girth]); }};'

    def get_random_scad(self):
       return self.scad.format(random.uniform(12e-2, 20e-2), random.uniform(0.03, 0.06))
