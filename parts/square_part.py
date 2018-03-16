import random
from math import sqrt
from parts import Part

class SquarePart(Part):
    def __init__(self,
                 min_length,
                 max_length,
                 min_width,
                 max_width,
                 min_depth,
                 max_depth):
        super(SquarePart, self).__init__(min_length, max_length, min_width, max_width,
                                          min_depth, max_depth)
        self.scad = 'thickness = {1}; cube([thickness, thickness, {0}], center=true);'

    def get_random_scad(self):
        self.depth = random.uniform(self.min_depth, self.max_depth)
        self.length = random.uniform(self.min_length, self.max_length)
        return self.scad.format(self.depth, self.length)
