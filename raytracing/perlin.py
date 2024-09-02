from . import randfloat, vec3
from math import floor


class Perlin:
    def __init__(self, point_count=256):
        self.pc = point_count
        self.rv = []
        for i in range(self.pc):
            self.rv.append(vec3.Vec3.random(-1, 1).normalized())
        self.px, self.py, self.pz = (self.gen_perm() for _ in range(3))

    def noise(self, point):
        i, j, k = (int(floor(x)) % self.pc for x in point)
        u, v, w = (q % self.pc for q in (point - vec3.Vec3(i, j, k)))
        c = [
            [
                [
                    self.rv[
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
        for i in range(len(p) - 1, -1, -1):
            t = randfloat.randint(0, i)
            p[i], p[t] = p[t], p[i]
        return p

    def trilinear(self, c, u, v, w):
        accum = 0
        uu, vv, ww = (x**2 * (3 - 2 * x) for x in (u, v, w))
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight = vec3.Vec3(u - i, v - j, w - k)
                    accum += (
                        (i * uu + (1 - i) * (1 - uu))
                        * (j * vv + (1 - j) * (1 - vv))
                        * (k * ww + (1 - k) * (1 - ww))
                        * c[i][j][k].dot(weight)
                    )
        return accum

    def turb(self, point, depth):
        accum = 0
        p = point
        weight = 1
        for i in range(depth):
            accum += weight * self.noise(p)
            weight *= 0.5
            p *= 2
        return abs(accum)
