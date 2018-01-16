import random
from part import Part

class RoundHandle(Part):
    def __init__(self):
        self.scad = 'translate([0,0, -{0}]) {{\n cylinder({0}, {1}, {2}, $fn=64);\n }};'

    def get_random_scad(self):
        if random.random() < 0.8:
            r = random.uniform(1e-2, 3.5e-2)
            return self.scad.format(random.uniform(12e-2, 37.5e-2), r, r)
        return self.scad.format(random.uniform(12e-2, 37.5e-2), random.uniform(1e-2, 3.5e-2),
                                random.uniform(1e-2, 3.5e-2))
