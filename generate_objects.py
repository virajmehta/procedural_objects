import sys
import os
import random
from subprocess import call
from pymesh import stl
from heads import RoundHead, SquareHead
from handles import RoundHandle, SquareHandle, TriangleHandle
import lib
from ipdb import set_trace as db


temp_head_fn = 'head.scad'
temp_handle_fn = 'handle.scad'
head_stl_fn = 'head.stl'
handle_stl_fn = 'handle.stl'
head_obj = 'head.obj'
handle_obj = 'handle.obj'
urdf_template_fn = 'template.urdf'
hammer_urdf = 'hammer.urdf'
scad_command = 'openscad -o {1} {0}'
MASS=2.


def generate_hammer(directory):
    # Sample heads and handles
    heads = [RoundHead(), SquareHead()]
    handles = [RoundHandle(), SquareHandle(), TriangleHandle()]
    head = random.choice(heads)
    handle = random.choice(handles)

    # write scad file with randomly parametrized dimensions
    head.write_scad(temp_head_fn)
    handle.write_scad(temp_handle_fn)

    # compile scad file with OpenScad into STL
    call(scad_command.format(temp_head_fn, head_stl_fn), shell=True)
    call(scad_command.format(temp_handle_fn, handle_stl_fn), shell=True)

    # read STL into pymesh
    head = stl.Stl(head_stl_fn)
    handle = stl.Stl(handle_stl_fn)

    # write OBJ from pymesh
    head_obj_fn = os.path.join(directory, head_obj)
    handle_obj_fn = os.path.join(directory, handle_obj)
    head.save_obj(head_obj_fn)
    handle.save_obj(handle_obj_fn)

    head_vertices, head_faces, _ = lib.read_mesh(head_obj_fn)
    handle_vertices, handle_faces, _ = lib.read_mesh(handle_obj_fn)
    head_com = lib.compute_centroid(head_vertices, head_faces)
    handle_com = lib.compute_centroid(handle_vertices, handle_faces)
    com = (head_com + handle_com) / 2

    with open(urdf_template_fn) as f:
        template = f.read()

    # write URDF with meshes etc
    urdf_fn = os.path.join(directory, hammer_urdf)
    with open(urdf_fn, 'w') as f:
        f.write(template.format(
                body_name='hammer',
                mass=MASS, ixx=1e-3, ixy=0.,
                ixz=0., iyy=1e-3, iyz=0.,
                izz=1e-3, head_file=head_obj_fn,
                handle_file=handle_obj_fn,
                cx=com[0], cy=com[1], cz=com[2]))

    # Clean up the temp files
    os.remove(temp_head_fn)
    os.remove(temp_handle_fn)
    os.remove(head_stl_fn)
    os.remove(handle_stl_fn)
    return urdf_fn

def generate_hammers(directory, num_hammers):
    dir_index = 0
    for i in range(num_hammers):
        while True:
            current_dir = os.path.join(directory, str(dir_index))
            if os.path.exists(current_dir):
                dir_index += 1
                continue
            os.mkdir(current_dir)
            break
        generate_hammer(current_dir)


if __name__== '__main__':
    generate_hammers(sys.argv[1], int(sys.argv[2]))

