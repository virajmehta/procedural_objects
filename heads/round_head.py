import random
from heads import Head


class RoundHead(Head):
    def __init__(self,
                 min_radius=1.5e-2,
                 max_radius=3e-2,
                 min_length=10e-2,
                 max_length=20e-2,
                 max_tilt=20,
                 z_offset=0,
                 constant_diameter_prob=0.7,
                 is_L=False,
                 is_X=False):
        super(RoundHead, self).__init__(max_radius, min_radius, max_length,
                                        min_length, max_tilt, z_offset,
                                        is_L, is_X)
        self.scad = 'length = {0};rotate(a=[0,{3},0]) {{translate([-length/2, 0., 0.]) {{ rotate(a=[0, 90, 0]) {{ cylinder(length, {1}, {2}, $fn=90); }} }} }};'  # NOQA
        self.constant_diameter_prob = constant_diameter_prob

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        if random.random() > self.constant_diameter_prob:
            tilt = random.uniform(-self.max_tilt, self.max_tilt)
        else:
            tilt = 0
        if random.random() < self.constant_diameter_prob:
            radius = random.uniform(self.min_radius, self.max_radius)
            return self.scad.format(length, radius, radius, tilt)
        radius1 = random.uniform(self.min_radius, self.max_radius)
        radius2 = random.uniform(self.min_radius, self.max_radius)
        return self.scad.format(length, radius1, radius2, tilt)

