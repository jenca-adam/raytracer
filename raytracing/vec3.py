from .randfloat import randfloat


def linear_to_gamma(linear):
    if linear > 0:
        return linear ** (0.5)
    return 0


class Vec3:
    def __init__(self, *e):
        self.x = self.r = e[0]
        self.y = self.g = e[1]
        self.z = self.b = e[2]
        self.e = e

    @property
    def length(self):
        return self.length_squared**0.5

    @property
    def length_squared(self):
        return self.x**2 + self.y**2 + self.z**2

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        return Vec3(
            self.e[1] * v.e[2] - self.e[2] * v.e[1],
            self.e[2] * v.e[0] - self.e[0] * v.e[2],
            self.e[0] * v.e[1] - self.e[1] * v.e[0],
        )

    def __add__(self, v):
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        return self + (-v)

    def __truediv__(self, s):
        return self * (1 / s)

    def __floordiv__(self, s):
        return Vec3(self.x // s, self.y // s, self.z // s)

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, s):
        return Vec3(self.x * s, self.y * s, self.z * s)

    def __rmul__(self, s):
        return self * s

    def __repr__(self):
        return f"({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def __iter__(self):
        return iter((self.x, self.y, self.z))

    def asrgb(self):
        return Vec3(int(self.x * 256), int(self.y * 256), int(self.z * 256))

    def normalized(self):
        return self / self.length

    def clamp_all(self, i):
        return Vec3(i.clamp(self.x), i.clamp(self.y), i.clamp(self.z))

    @classmethod
    def random(cls, min=0, max=1):
        return cls(randfloat(min, max), randfloat(min, max), randfloat(min, max))

    @classmethod
    def random_unit(cls):
        while True:
            p = cls.random(-1, 1)
            lsq = p.length_squared
            if 1e-160 < lsq <= 1:
                return p.normalized()

    @classmethod
    def random_on_hemisphere(cls, normal):
        u = cls.random_unit()
        if u.dot(normal) > 0:
            return u
        return -u

    @classmethod
    def random_in_unit_disk(cls):
        while True:
            p = cls(randfloat(-1, 1), randfloat(-1, 1), 0)
            if p.length_squared < 1:
                return p

    def gamma_corrected(self):
        return Vec3(
            linear_to_gamma(self.x), linear_to_gamma(self.y), linear_to_gamma(self.z)
        )

    def near_zero(self):
        return abs(self.x) < 1e-8 and abs(self.y) < 1e-8 and abs(self.z) < 1e-8

    def reflect(self, v):
        return self - 2 * self.dot(v) * v

    def item_mul(self, v):
        return Vec3(self.x * v.x, self.y * v.y, self.z * v.z)

    @classmethod
    def refract(cls, uv, n, etai_over_etat):
        cos_theta = min(-uv.dot(n), 1)
        r_out_perp = etai_over_etat * (uv + cos_theta * n)
        r_out_par = -((abs(1 - r_out_perp.length_squared)) ** 0.5) * n
        return r_out_perp + r_out_par
