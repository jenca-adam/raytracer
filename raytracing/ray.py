class Ray:
    def __init__(self, origin, dir):
        self.origin = origin
        self.dir = dir

    def at(self, t):
        return self.origin + self.dir * t
