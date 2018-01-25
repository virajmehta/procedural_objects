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
                 no_tilt_prob=0.7):
        super(BreadHead, self).__init__(max_radius, min_radius, max_length,
                                        min_length, max_tilt, z_offset)
        self.no_tilt_prob = no_tilt_prob
        self.scad = 'l = {0}; w = {1}; rotate(a=[0,{2},0]){{rotate(a=[90,0,0]){{translate([0,0, - l/2]){{linear_extrude(height=l, $fn=60) {{ translate([0, w/2.6, 0]) {{ circle(w/2); }} translate([-w/2, -w/2, 0]) {{ square(w); }} }} }} }} }}' # NOQA

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        radius = random.uniform(self.min_radius, self.max_radius)
        if random.random() > self.no_tilt_prob:
            tilt = random.uniform(-self.max_tilt, self.max_tilt)
        else:
            tilt = 0
        return self.scad.format(length, radius, tilt)

