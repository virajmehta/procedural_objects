import sys
import os
import random
from subprocess import call
from pymesh import stl
from heads import RoundHead, SquareHead
from handles import RoundHandle, SquareHandle, TriangleHandle


temp_head_fn = 'head.scad'
temp_handle_fn = 'handle.scad'
head_stl_fn = 'head.stl'
handle_stl_fn = 'handle.stl'
head_obj = 'head.obj'
handle_obj = 'handle.obj'
hammer_obj = 'hammer.obj'
urdf_template_fn = 'template.urdf'
hammer_urdf = 'hammer.urdf'
scad_command = 'openscad -o {1} {0}'
MASS=2.


def generate_hammer(directory):
    heads = [RoundHead(), SquareHead()]
    handles = [RoundHandle(), SquareHandle(), TriangleHandle()]
    head = random.choice(heads)
    handle = random.choice(handles)
    head.write_scad(temp_head_fn)
    handle.write_scad(temp_handle_fn)
    call(scad_command.format(temp_head_fn, head_stl_fn), shell=True)
    call(scad_command.format(temp_handle_fn, handle_stl_fn), shell=True)
    head = stl.Stl(head_stl_fn)
    handle = stl.Stl(handle_stl_fn)
    head_obj_fn = os.path.join(directory, head_obj)
    handle_obj_fn = os.path.join(directory, handle_obj)
    hammer_obj_fn = os.path.join(directory, hammer_obj)
    head.save_obj(head_obj_fn)
    handle.save_obj(handle_obj_fn)
    head.join(handle)
    head.save_obj(hammer_obj_fn)
    with open(urdf_template_fn) as f:
        template = f.read()
    urdf_fn = os.path.join(directory, hammer_urdf)
    with open(urdf_fn, 'w') as f:
        f.write(template.format(
                body_name='hammer',
                mass=MASS, ixx=1., ixy=0.,
                ixz=0., iyy=1., iyz=0.,
                izz=1., head_file=head_obj_fn,
                handle_file=handle_obj_fn))
    os.remove(temp_head_fn)
    os.remove(temp_handle_fn)
    os.remove(head_stl_fn)
    os.remove(handle_stl_fn)
    return urdf_fn

def generate_hammers(directory, num_hammers):
    for i in range(num_hammers):
        current_dir = os.path.join(directory, str(i))
        os.mkdir(current_dir)
        generate_hammer(current_dir)


if __name__== '__main__':
    generate_hammer(sys.argv[1], sys.argv[2])

