import random
from part import Part

class SquareHandle(Part):
    def __init__(self):
        self.scad = 'thickness = {1};\n translate([thickness / -2, thickness / -2, -{0}]) {{\n cube([thickness, thickness, {0}]);\n }};'

    def get_random_scad(self):
        return self.scad.format(random.uniform(12e-2, 37.5e-2), random.uniform(1e-2, 4e-2))
