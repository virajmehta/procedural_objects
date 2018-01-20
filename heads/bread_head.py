import random
from heads import Head

class BreadHead(Head):
    def __init__(self,
                 min_radius=1.5e-2,
                 max_radius=4e-2,
                 min_length=10e-2,
                 max_length=20e-2,
                 z_offset=0):
        super(BreadHead, self).__init__(max_radius, min_radius, max_length, min_length, z_offset)
        self.scad = 'l = {0}; w = {1}; rotate(a=[90,0,0]){{translate([0,0, - l/2]){{linear_extrude(height=l, $fn=60) {{ translate([0, w/2.6, 0]) {{ circle(w/2); }} translate([-w/2, -w/2, 0]) {{ square(w); }} }} }} }}'

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        radius = random.uniform(self.min_radius, self.max_radius)
        return self.scad.format(length, radius)

