from objects import Object

class HammerObject(Object):
    def __init__(self, parts=None, tilt_prob=0.7, max_tilt=20):
        super(TObject, self).__init__(parts)
        self.tilt_prob = tilt_prob
        self.max_tilt = 20

    def write_objs(self, path):
        head_part = random.choice(self.parts)
        handle_part = random.choice(self.parts)
        folder = os.path.dirname(path)
        head_fn = os.path.join(folder, 'head.obj')
        handle_fn = os.path.join(folder, 'handle.obj')
        head_part.write_obj(head_fn)
        handle_part.write_obj(handle_fn)
        return head_part, handle_part
