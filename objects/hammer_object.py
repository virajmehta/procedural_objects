import os
from objects import Object
from parts import ConvexPart, RoundPart, SquarePart, TrianglePart, BreadPart
import random


MIN_HANDLE_DEPTH=12e-2
MAX_HANDLE_DEPTH=28e-2
MIN_HANDLE_WIDTH=2e-2
MAX_HANDLE_WIDTH=5e-2
MIN_HANDLE_LENGTH=2e-2
MAX_HANDLE_LENGTH=5e-2
MIN_HEAD_DEPTH=10e-2
MAX_HEAD_DEPTH=20e-2
MIN_HEAD_WIDTH=3e-2
MAX_HEAD_WIDTH=6e-2
MIN_HEAD_LENGTH=3e-2
MAX_HEAD_LENGTH=6e-2


class HammerObject(Object):

    HEAD_MASS = (0.8, 1.4)
    HANDLE_MASS = (0.5, 1.1)
    def __init__(self, parts=None, tilt_prob=0.7, max_tilt=20):
        super(HammerObject, self).__init__([])
        self.handle_parts = [ConvexPart(min_length=MIN_HANDLE_LENGTH,
                                        max_length=MAX_HANDLE_LENGTH,
                                        min_width=3e-2,
                                        max_width=6e-2,
                                        min_depth=3e-2,
                                        max_depth=6e-2),
                             RoundPart(min_length=MIN_HANDLE_LENGTH,
                                       max_length=MAX_HANDLE_LENGTH,
                                       min_width=MIN_HANDLE_WIDTH,
                                       max_width=MAX_HANDLE_WIDTH,
                                       min_depth=MIN_HANDLE_DEPTH,
                                       max_depth=MAX_HANDLE_DEPTH),
                             SquarePart(min_length=MIN_HANDLE_LENGTH,
                                        max_length=MAX_HANDLE_LENGTH,
                                        min_width=MIN_HANDLE_WIDTH,
                                        max_width=MAX_HANDLE_WIDTH,
                                        min_depth=MIN_HANDLE_DEPTH,
                                        max_depth=MAX_HANDLE_DEPTH),
                             TrianglePart(min_length=MIN_HANDLE_LENGTH,
                                        max_length=MAX_HANDLE_LENGTH,
                                        min_width=MIN_HANDLE_WIDTH,
                                        max_width=MAX_HANDLE_WIDTH,
                                        min_depth=MIN_HANDLE_DEPTH,
                                        max_depth=MAX_HANDLE_DEPTH),
                             BreadPart(min_length=MIN_HANDLE_LENGTH,
                                        max_length=MAX_HANDLE_LENGTH,
                                        min_width=MIN_HANDLE_WIDTH,
                                        max_width=MAX_HANDLE_WIDTH,
                                        min_depth=MIN_HANDLE_DEPTH,
                                        max_depth=MAX_HANDLE_DEPTH)]
        self.head_parts = [ConvexPart(min_length=8e-2,
                                      max_length=15e-2,
                                      min_width=4e-2,
                                      max_width=8e-2,
                                      min_depth=4e-2,
                                      max_depth=8e-2),
                             RoundPart(min_length=MIN_HEAD_LENGTH,
                                       max_length=MAX_HEAD_LENGTH,
                                       min_width=MIN_HEAD_WIDTH,
                                       max_width=MAX_HEAD_WIDTH,
                                       min_depth=MIN_HEAD_DEPTH,
                                       max_depth=MAX_HEAD_DEPTH),
                             SquarePart(min_length=MIN_HEAD_LENGTH,
                                        max_length=MAX_HEAD_LENGTH,
                                        min_width=MIN_HEAD_WIDTH,
                                        max_width=MAX_HEAD_WIDTH,
                                        min_depth=MIN_HEAD_DEPTH,
                                        max_depth=MAX_HEAD_DEPTH),
                             TrianglePart(min_length=MIN_HEAD_LENGTH,
                                        max_length=MAX_HEAD_LENGTH,
                                        min_width=MIN_HEAD_WIDTH,
                                        max_width=MAX_HEAD_WIDTH,
                                        min_depth=MIN_HEAD_DEPTH,
                                        max_depth=MAX_HEAD_DEPTH),
                             BreadPart(min_length=MIN_HEAD_LENGTH,
                                        max_length=MAX_HEAD_LENGTH,
                                        min_width=MIN_HEAD_WIDTH,
                                        max_width=MAX_HEAD_WIDTH,
                                        min_depth=MIN_HEAD_DEPTH,
                                        max_depth=MAX_HEAD_DEPTH)]

        self.tilt_prob = tilt_prob
        self.max_tilt = 20

    def write_objs(self, path):
        head_part = random.choice(self.head_parts)
        handle_part = random.choice(self.handle_parts)
        folder = os.path.dirname(path)
        head_fn = os.path.join(folder, 'head.obj')
        handle_fn = os.path.join(folder, 'handle.obj')
        head_part.write_obj(head_fn)
        handle_part.write_obj(handle_fn)
        return head_part, handle_part
