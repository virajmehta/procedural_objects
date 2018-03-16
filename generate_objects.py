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


# temporary filenames for the process
head_obj = 'head.obj'
handle_obj = 'handle.obj'
urdf_template_fn = 'template.urdf'
hammer_urdf = 'hammer.urdf'
HEAD_MASS = (0.8, 1.4)
HANDLE_MASS = (0.5, 1.1)
ROLL_SPIN_FRIC = (0.5e-3, 5e-3)
LAT_FRIC = (3., 6.)


'''
def generate_hammer(directory, heads, handles):
    directory = os.path.abspath(directory)
    print('generating hammer in %s' % (directory))
    head = random.choice(heads)
    handle = random.choice(handles)

    # write OBJ from Part
    head_obj_fn = os.path.join(directory, head_obj)
    handle_obj_fn = os.path.join(directory, handle_obj)
    head.write_obj(head_obj_fn)
    handle.write_obj(handle_obj_fn)

    head_vertices, head_faces, _ = lib.read_mesh(head_obj_fn)
    handle_vertices, handle_faces, _ = lib.read_mesh(handle_obj_fn)
    head_com = lib.compute_centroid(head_vertices, head_faces)
    handle_com = lib.compute_centroid(handle_vertices, handle_faces)

    with open(urdf_template_fn) as f:
        template = f.read()

    # write URDF with meshes etc
    urdf_fn = os.path.join(directory, hammer_urdf)
    head_mass = random.uniform(*HEAD_MASS)
    handle_mass = random.uniform(*HANDLE_MASS)
    lat_fric = 0.2  # random.uniform(*LAT_FRIC)
    roll_spin_fric = 0.2  # random.uniform(*ROLL_SPIN_FRIC)
    with open(urdf_fn, 'w') as f:
        f.write(template.format(
                body_name='hammer',
                handle_mass=handle_mass,
                head_mass=head_mass,
                ixx=1,
                ixy=0.,
                ixz=0.,
                iyy=1,
                iyz=0.,
                izz=1,
                head_file=os.path.basename(head_obj_fn),
                handle_file=os.path.basename(handle_obj_fn),
                handle_cx=handle_com[0],
                handle_cy=handle_com[1],
                handle_cz=handle_com[2],
                head_cx=head_com[0],
                head_cy=head_com[1],
                head_cz=head_com[2],
                lat_fric=lat_fric,
                roll_spin_fric=roll_spin_fric))

    return urdf_fn
'''


def generate_hammers(directory, num_hammers, object_type=None,
                     difficulty=None):
    num_hammers = int(num_hammers)
    # Sample heads and handles
    assert object_type in ('L', 'X', 'T', None)
    assert difficulty in ('E', 'M', 'H', None)
    is_L = object_type == 'L'
    is_X = object_type == 'X'
    if difficulty == 'E':
        heads = [RoundHead(is_L=is_L, is_X=is_X), SquareHead(is_L=is_L,
                 is_X=is_X), BreadHead(is_L=is_L, is_X=is_X)]
        handles = [RoundHandle(), SquareHandle(), TriangleHandle()]
    elif difficulty == 'M':
        heads = [ConvexHead(is_L=is_L, is_X=is_X)]
        handles = [RoundHandle(), SquareHandle(), TriangleHandle()]
    elif difficulty == 'H':
        heads = [ConvexHead(is_L=is_L, is_X=is_X)]
        handles = [ConvexHandle()]
    else:
        heads = [RoundHead(), SquareHead(), BreadHead(), ConvexHead()]
        handles = [RoundHandle(), SquareHandle(), TriangleHandle(),
                   ConvexHandle()]
    dir_index = 0
    for i in range(num_hammers):
        while True:
            current_dir = os.path.join(directory, str(dir_index))
            if os.path.exists(current_dir):
                dir_index += 1
                continue
            os.mkdir(current_dir)
            break
        generate_hammer(current_dir, heads, handles)


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
    '''
    if len(sys.argv) == 3:
        generate_hammers(*sys.argv[1:3])
    elif len(sys.argv) == 4:
        generate_hammers(*sys.argv[1:4])
    elif len(sys.argv) == 5:
        generate_hammers(*sys.argv[1:5])
    else:
        raise Exception('nope')
    '''
    generate_objects(*sys.argv[1:])
