import random
from part import Part

class TriangleHandle(Part):
    def __init__(self):
        self.scad = 'translate([0,0, -{0}]) {{\ncylinder({0}, {1}, $fn=3);\n}};'
    def get_random_scad(self):
        return self.scad.format(random.uniform(12e-2, 37.5e-2), random.uniform(2e-2, 5e-2))
