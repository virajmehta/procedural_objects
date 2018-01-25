import random
from math import sqrt
from handles import Handle

class SquareHandle(Handle):
    def __init__(self,
                 min_length=12e-2,
                 max_length=37.5e-2,
                 min_radius=1.5e-2,
                 max_radius=3e-2):
        super(SquareHandle, self).__init__(min_length, max_length, min_radius, max_radius)
        self.scad = 'thickness = {1};\n translate([thickness / -2, thickness / -2, -{0}]) {{\n cube([thickness, thickness, {0}]);\n }};'
        self.min_square_side_length = min_radius * sqrt(2)
        self.max_square_side_length = max_radius * sqrt(2)

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        square_side_length = random.uniform(self.min_square_side_length, self.max_square_side_length)
        return self.scad.format(length, square_side_length)
