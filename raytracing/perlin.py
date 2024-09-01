from . import randfloat, vec3


class Perlin:
    def __init__(self, point_count=256):
        self.pc = point_count
        self.rf = []
        for i in range(self.pc):
            self.rf.append(randfloat.randfloat())
        self.px, self.py, self.pz = (self.gen_perm() for _ in range(3))

    def noise(self, point):
        i, j, k = map(int, point)
        u, v, w = point - vec3.Vec3(i, j, k)
        c = [
            [
                [
                    self.rf[
                        self.px[(i + di) & 255]
                        ^ self.py[(j + dj) & 255]
                        ^ self.pz[(k + dk) & 255]
                    ]
                    for dk in range(2)
                ]
                for dj in range(2)
            ]
            for di in range(2)
        ]
        return self.trilinear(c, u, v, w)

    def gen_perm(self):
        return self.permute(range(self.pc))

    def permute(self, p):
        p = list(p)
        for i in range(self.pc - 1, 0, -1):
            t = randfloat.randint(0, i)
            p[i], p[t] = p[t], p[i]
        return p

    def trilinear(self, c, u, v, w):
        accum = 0
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    accum += (
                        (i * u + (1 - i) * (1 - u))
                        * (j * v + (1 - j) * (1 - v))
                        * (k * w + (1 - k) * (1 - w))
                        * c[i][j][k]
                    )
        return accum
