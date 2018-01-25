import random
from part import Part

class Head(Part):
    def __init__(self, min_radius, max_radius, min_length, max_length, max_tilt, z_offset=0):
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_length = min_length
        self.max_length = max_length
        self.max_tilt = max_tilt
        self.z_offset = z_offset

