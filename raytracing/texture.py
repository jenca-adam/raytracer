from PIL import Image as PILImage
from numpy import float64, asarray
import sys
from . import vec3, interval, perlin


class Texture:
    @classmethod
    def texturify(cls, obj):
        c = obj.__class__
        if issubclass(c, cls):
            return obj
        return SolidColor(obj)


class SolidColor(Texture):
    def __init__(self, albedo):
        self.albedo = albedo

    def sample(self, u, v, p):
        return self.albedo


class Checkered(Texture):
    def __init__(self, scale, even, odd):
        self.inv_scale = 1 / scale
        self.even = even
        self.odd = odd

    def sample(self, u, v, p):
        xi, yi, zi = map(int, self.inv_scale * p)
        if (xi + yi + zi) % 2:
            return self.odd.sample(u, v, p)
        return self.even.sample(u, v, p)


class Image(Texture):
    def __init__(self, path):
        try:
            self.img_data = asarray(PILImage.open(path))
        except:
            self.img_data = None

    def sample(self, u, v, p):
        if self.img_data is None:
            return vec3.Vec3(1, 0, 0)
        u = interval.Interval(0, 1).clamp(u)
        v = 1 - interval.Interval(0, 1).clamp(v)
        i = u * len(self.img_data[0])
        j = v * len(self.img_data)
        # print(i,j,u,v,file=sys.stderr)
        pixel = self.img_data[int(j) - 1][int(i) - 1]
        return (1 / 255) * vec3.Vec3(*pixel)


class Noise(Texture):
    def __init__(self):
        self.noise = perlin.Perlin()

    def sample(self, u, v, p):
        return vec3.Vec3(1, 1, 1) * self.noise.noise(p)
