

class Part(object):
    def __init__(self):
        pass

    def get_random_scad(self):
        return ''

    def write_scad(self, fn):
        with open(fn, 'w') as f:
            f.write(self.get_random_scad())


