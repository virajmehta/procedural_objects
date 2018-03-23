'''
Procedural Object Generation
Viraj Mehta, 2018

This program generates procedural objects as URDFs and objs
for use in robot simulations.

Invocation:
python generate_objects.py (1) (2) (3?) (4?)

(1): the directory in which to generate objects
     it will be filled with numeric subdirectories which are self-referencing
     URDFs, i.e. directory/1/hammer.urdf, directory/2/hammer.urdf, ...

(2): the number of URDFs to generate

(3)(optional): a string in ('L', 'T', 'X') which enforces a given topology
               of hammer
(4)(optional): a string in ('E', 'M', 'H') which enforces a difficulty level as
               defined below

E(asy): parametric object and handle
M(edium): parametric handle, convex head
H(ard): convex handle, convex head

Pipeline:
1. random parts are chosen as heads and handles
2. random parameters are sampled and .scad files are written that contain them
3. Using OpenSCAD, these are compiled to .stl files.
4. Using pymesh (the less nice version), these are turned into .obj files
5. We compute the approximate centroid and sample random physical parameters
6. This is all written as a URDF
'''
import sys
import os
import random
from objects import TObject
import lib


def generate_object(directory):
    path = os.path.join(directory, 'object.urdf')
    objects = [TObject()]
    obj = random.choice(objects)
    obj.generate_urdf(path)



def generate_objects(directory, num_objects):
    num_objects = int(num_objects)
    dir_index = 0
    for i in range(num_objects):
        while True:
            current_dir = os.path.join(directory, str(dir_index))
            if os.path.exists(current_dir):
                dir_index += 1
                continue
            os.mkdir(current_dir)
            break
        generate_object(current_dir)



if __name__ == '__main__':
    generate_objects(*sys.argv[1:])
