import random
from heads import Head

class StickHead(Head):
    def __init__(self,
                 min_radius=1.5e-2,
                 max_radius=4e-2,
                 min_length=7-2,
                 max_length=15e-2,
                 z_offset=0,
                 constant_diameter_prob=0.7):
        super(StickHead, self).__init__(max_radius, min_radius, max_length, min_length, z_offset)
        self.scad = ['length = {0}; cylinder(length, {1}, {2}, $fn=90);',
                    'length = {0};cylinder(length, {1}, {2}, $fn=3);']


        self.constant_diameter_prob = constant_diameter_prob

    def get_random_scad(self):
        length = random.uniform(self.min_length, self.max_length)
        if random.random() < self.constant_diameter_prob:
            radius = random.uniform(self.min_radius, self.max_radius)
            return random.choice(self.scad).format(length, radius, radius)
        radius1 = random.uniform(self.min_radius, self.max_radius)
        radius2 = random.uniform(self.min_radius, self.max_radius)
        return random.choice(self.scad).format(length, radius1, radius2)
