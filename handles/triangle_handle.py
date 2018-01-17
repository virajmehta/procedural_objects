import random
from handles import Handle

class TriangleHandle(Handle):
    def __init__(self,
                 min_length=12e-2,
                 max_length=37.5e-2,
                 min_radius=1e-2,
                 max_radius=4e-2,
                 constant_diameter_prob=0.7):
        super(TriangleHandle, self).__init__(min_length, max_length, min_radius, max_radius)
        self.scad = 'translate([0,0, -{0}]) {{\n cylinder({0}, {1}, {2}, $fn=64);\n }};'
        self.constant_diameter_prob = constant_diameter_prob

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        if random.random() < self.constant_diameter_prob:
            radius = random.uniform(self.min_radius, self.max_radius)
            return self.scad.format(length, radius, radius)
        radius1 = random.uniform(self.min_radius, self.max_radius)
        radius2 = random.uniform(self.min_radius, self.max_radius)
        return self.scad.format(length, radius1, radius2)
