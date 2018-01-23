import os
from subprocess import call
from pymesh import stl


temp_scad_fn = 'temp.scad'
temp_stl_fn = 'temp.stl'
scad_command = 'openscad -o {1} {0}'
class Part(object):
    def __init__(self):
        pass

    def get_random_scad(self):
        assert False
        return ''

    def write_scad(self, fn):
        with open(fn, 'w') as f:
            f.write(self.get_random_scad())

    def write_obj(self, fn):
        self.write_scad(temp_scad_fn)
        call(scad_command.format(temp_scad_fn, temp_stl_fn), shell=True)
        part = stl.Stl(temp_stl_fn)
        part.save_obj(fn)
        os.remove(temp_scad_fn)
        os.remove(temp_stl_fn)


