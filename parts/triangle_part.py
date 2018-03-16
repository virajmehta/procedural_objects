import random
from parts import Part


class TrianglePart(Part):
    def __init__(self,
                 min_length,
                 max_length,
                 min_width,
                 max_width,
                 min_depth,
                 max_depth,
                 constant_diameter_prob=0.7):
        super(TrianglePart, self).__init__(min_length, max_length, min_width, max_width,
                                           min_depth, max_depth)
        self.scad = 'translate([0,0, -{0} / 2]) {{\n cylinder({0}, {1}, {2}, $fn=64);\n }};'  # NOQA
        self.constant_diameter_prob = constant_diameter_prob

    def get_random_scad(self):
        self.depth = random.uniform(self.min_depth, self.max_depth)
        min_radius = self.min_width / 1.5
        max_radius = self.min_width / 1.5
        if random.random() < self.constant_diameter_prob:
            radius = random.uniform(min_radius, max_radius)
            self.width = radius * 1.5
            self.length = radius * 1.5
            return self.scad.format(self.depth, radius, radius)
        radius1 = random.uniform(min_radius, max_radius)
        radius2 = random.uniform(min_radius, max_radius)
        self.width = max(radius1, radius2) * 1.5
        self.length = self.width
        return self.scad.format(length, radius1, radius2)
