import random
from parts import Part


class BreadPart(Part):
    def __init__(self,
                 min_length,
                 max_length,
                 min_width,
                 max_width,
                 min_depth,
                 max_depth):
        super(BreadPart, self).__init__(min_length, max_length, min_width, max_width, min_depth,
                max_depth)
        self.scad = 'l = {0}; w = {1}; translate([0, 0, -l/2]) {{ linear_extrude(height=l, $fn=60) {{ translate([-w/2.6,0,0]) {{ circle(w/2); }} translate([-w/2, -w/2, 0]) {{ square(w); }} }} }}'

    def get_random_scad(self):
        self.depth = random.uniform(self.min_depth, self.max_depth)
        self.length = random.uniform(self.min_length, self.max_length)
        self.width = self.length
        return self.scad.format(self.depth, self.length)

