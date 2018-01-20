'''
Procedural Object Generation
Viraj Mehta, 2018

This program generates procedural objects as URDFs and objs
for use in robot simulations.

Invocation:
python generate_objects.py (1) (2)

(1): the directory in which to generate objects
     it will be filled with numeric subdirectories which are self-referencing
     URDFs, i.e. directory/1/hammer.urdf, directory/2/hammer.urdf, ...

(2): the number of URDFs to generate

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
from heads import RoundHead, SquareHead, ConvexHead, BreadHead
from handles import RoundHandle, SquareHandle, TriangleHandle
import lib


# temporary filenames for the process
head_obj = 'head.obj'
handle_obj = 'handle.obj'
urdf_template_fn = 'template.urdf'
hammer_urdf = 'hammer.urdf'
MASS=(0.75, 2.25)
ROLL_SPIN_FRIC=(0.5e-3, 5e-3)
LAT_FRIC=(3., 6.)


def generate_hammer(directory, heads, handles):
    directory = os.path.abspath(directory)
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
    # center of mass
    com = (head_com + handle_com) / 2

    with open(urdf_template_fn) as f:
        template = f.read()

    # write URDF with meshes etc
    urdf_fn = os.path.join(directory, hammer_urdf)
    mass = random.uniform(*MASS)
    lat_fric = random.uniform(*LAT_FRIC)
    roll_spin_fric = random.uniform(*ROLL_SPIN_FRIC)
    with open(urdf_fn, 'w') as f:
        f.write(template.format(
                body_name='hammer',
                mass=mass,
                ixx=1,
                ixy=0.,
                ixz=0.,
                iyy=1,
                iyz=0.,
                izz=1,
                head_file=head_obj_fn,
                handle_file=handle_obj_fn,
                cx=com[0],
                cy=com[1],
                cz=com[2],
                lat_fric=lat_fric,
                roll_spin_fric=roll_spin_fric))

    return urdf_fn

def generate_hammers(directory, num_hammers):
    # Sample heads and handles
    heads = [BreadHead()]
    #heads = [ConvexHead(), RoundHead(), SquareHead()]
    handles = [RoundHandle(), SquareHandle(), TriangleHandle()]
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


if __name__== '__main__':
    generate_hammers(sys.argv[1], int(sys.argv[2]))

