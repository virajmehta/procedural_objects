'''
Part is always going to be length - X, width - Y, depth- Z
aligned with the center exactly at the origin.
'''
import os
from subprocess import call
from pymesh import stl
import random


scad_command = 'openscad -o {1} {0}'


class Part(object):
    def __init__(self,
                 min_length,
                 max_length,
                 min_width,
                 max_width,
                 min_depth,
                 max_depth):
        self.min_length = min_length
        self.max_length = max_length
        self.min_width = min_width
        self.max_width = max_width
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.length = None
        self.width = None
        self.depth = None
        self.fn = None

    def get_random_scad(self):
        return ''



    def write_scad(self, fn):
        with open(fn, 'w') as f:
            f.write(self.get_random_scad())

    # can be overwritten
    def write_obj(self, fn):
        self.fn = fn
        temp_scad_fn = '%d.scad' % random.randint(0, 10000000000)
        temp_stl_fn = '%d.stl' % random.randint(0, 1000000000)
        self.write_scad(temp_scad_fn)
        call(scad_command.format(temp_scad_fn, temp_stl_fn), shell=True)
        part = stl.Stl(temp_stl_fn)
        part.save_obj(fn)
        os.remove(temp_scad_fn)
        os.remove(temp_stl_fn)


