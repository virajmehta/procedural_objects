import random
from heads import Head

class RoundHead(Head):
    def __init__(self,
                 min_radius=1.5e-2,
                 max_radius=4e-2,
                 min_length=10e-2,
                 max_length=20e-2,
                 z_offset=0,
                 constant_diameter_prob=0.7):
        super(RoundHead, self).__init__(max_radius, min_radius, max_length, min_length, z_offset)
        self.scad = 'length = {0};translate([-length/2, 0., 0.]) {{ rotate(a=[0, 90, 0]) {{ cylinder(length, {1}, {2}, $fn=90); }} }};'
        self.constant_diameter_prob = constant_diameter_prob

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        if random.random() < self.constant_diameter_prob:
            radius = random.uniform(self.min_radius, self.max_radius)
            return self.scad.format(length, radius, radius)
        radius1 = random.uniform(self.min_radius, self.max_radius)
        radius2 = random.uniform(self.min_radius, self.max_radius)
        return self.scad.format(length, radius1, radius2)

