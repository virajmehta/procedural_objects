import random
from part import Part

class RoundHead(Part):
    def __init__(self):
        self.scad = 'length = {0};translate([-length/2, 0., 0.]) {{ rotate(a=[0, 90, 0]) {{ cylinder(length, {1}, {2}, $fn=90); }}; }};'
    def get_random_scad(self):
        if random.random() < 0.8:
            r = random.uniform(0.015, 0.04)
            return self.scad.format(random.uniform(10e-2, 20e-02), r, r)
        return self.scad.format(random.uniform(10e-2, 20e-2), random.uniform(0.015, 0.04),
                                random.uniform(0.015, 0.04))

