from parts import *
import constants

class Object(object):
    COLOR = (0.5,0.5,0.5)
    def __init__(self, parts=None):
        if parts is None:
            self.parts = [BreadPart(), ConvexPart(), SquarePart(), RoundPart(), TrianglePart()]
        else:
            self.parts = parts

    def generate_urdf(self, path):
        raise NotImplementedError()

    def get_link(self, name,  mass, filename, roll=0, pitch=0,
            yaw=0, cx=0, cy=0, cz=0, x=0, y=0, z=0, red=None,
            green=None, blue=None, lat_fric=constants.lat_fric,
            roll_spin_fric=constants.roll_spin_fric):
        with open('templates/mesh_template') as f:
            mesh_template = f.read()
        if red is None:
            red = self.COLOR[0]
        if blue is None:
            blue = self.COLOR[1]
        if green is None:
            green = self.COLOR[2]
        link = mesh_template.format(name='head',
                                   lat_fric=lat_fric,
                                   roll_spin_fric=roll_spin_fric,
                                   roll=roll,
                                   pitch=pitch,
                                   yaw=yaw,
                                   cx=cx,
                                   cy=cy,
                                   cz=cz,
                                   x=x,
                                   y=y,
                                   z=z,
                                   mass=mass,
                                   filename=filename,
                                   red=red,
                                   blue=blue,
                                   green=green)
        return link

    def get_joint(self, parent_name, child_name):
        with open('templates/joint_template') as f:
            joint_template = f.read()
        joint = joint_template.format(parent_name=parent_name,
                                      child_name=child_name)
        return joint

    def get_urdf(self, body_name, links, joints):
        with open('templates/template.urdf') as f:
            urdf_template = f.read()
        urdf = urdf_template.format(body_name=body_name, links=links,
                joints=joints)
        return urdf

        
