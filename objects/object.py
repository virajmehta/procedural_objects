from parts import *

class Object(object):
    def __init__(self, parts=None):
        if parts is None:
            self.parts = [BreadPart(), ConvexPart(), SquarePart(), RoundPart(), TrianglePart()]
        else:
            self.parts = parts

    def generate_urdf(self, path):
        raise NotImplementedError()

        
