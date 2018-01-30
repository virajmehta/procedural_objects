import random
from heads import Head


class BreadHead(Head):
    def __init__(self,
                 min_radius=1.5e-2,
                 max_radius=3e-2,
                 min_length=10e-2,
                 max_length=20e-2,
                 max_tilt=20,
                 z_offset=0,
                 no_tilt_prob=0.2,
                 is_L=False,
                 is_X=False):
        super(BreadHead, self).__init__(min_radius, max_radius, min_length,
                                        max_length, max_tilt, z_offset, is_L,
                                        is_X)
        self.no_tilt_prob = no_tilt_prob
        self.scad = 'l = {0}; w = {1}; translate([{3}, 0, {4}]) {{rotate(a=[{5},{2},0]){{rotate(a=[0,90,0]){{translate([0,0, - l/2]){{linear_extrude(height=l, $fn=60) {{ translate([-w/2.6,0,0]) {{ circle(w/2); }} translate([-w/2, -w/2, 0]) {{ square(w); }} }} }} }} }} }};' # NOQA 

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        radius = random.uniform(self.min_radius, self.max_radius)
        tilt = 0
        roll = 0
        z_offset = 0
        x_offset = 0
        if random.random() > self.no_tilt_prob:
            tilt = random.uniform(-self.max_tilt, self.max_tilt)
            roll = random.uniform(-self.max_tilt, self.max_tilt)
        if self.is_L:
            x_offset = (length / 2) - 3e-2
            tilt = 0
        if self.is_X:
            z_offset = random.uniform(-15e-2, 0)
        return self.scad.format(length, radius, tilt, x_offset, z_offset, roll)

