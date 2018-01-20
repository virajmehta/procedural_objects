import random
from part import Part

class Handle(Part):
    def __init__(self, min_length, max_length, min_radius, max_radius):
        self.min_length = min_length
        self.max_length = max_length
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.scad = None
