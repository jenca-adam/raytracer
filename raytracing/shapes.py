from collections import namedtuple
import math

HitResult = namedtuple(
    "HitResult",
    ("p", "normal", "t", "front_face", "material", "u", "v"),
    defaults=(None, None, None, None, None, None, None),
)


class Hittable:
    def hit(self, *args):
        hit, *hr = self._hit(*args)
        return hit, HitResult(*hr)

    def _hit(self, *args):
        raise NotImplementedError("can't call hit on plain Hittable instance")


class Sphere(Hittable):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def _hit(self, ray, ray_tmin, ray_tmax):
        oc = self.center - ray.origin
        a = ray.dir.length_squared
        h = ray.dir.dot(oc)
        c = oc.length_squared - self.radius**2
        d = h**2 - a * c
        if d < 0:
            return (False,)
        sqrtd = d ** (0.5)
        root = (h - sqrtd) / a
        if root <= ray_tmin or ray_tmax <= root:
            root = (h + sqrtd) / a
            if root <= ray_tmin or ray_tmax <= root:
                return (False,)
        p = ray.at(root)
        outward_normal = (p - self.center) / self.radius
        is_front = ray.dir.dot(outward_normal) < 0
        normal = (-1) ** (not is_front) * outward_normal
        return (
            True,
            p,
            normal,
            root,
            is_front,
            self.material,
            *self.getuv(normal),
        )

    def getuv(self, p):
        theta, phi = math.acos(-p.y), math.atan2(-p.z, p.x) + math.pi
        u = phi / (2 * math.pi)
        v = theta / math.pi
        return u, v


class Quad(Hittable):
    def __init__(self, q, u, v, material):
        n = u.cross(v)
        self.q = q
        self.u = u
        self.v = v
        self.material = material
        self.normal = n.normalized()
        self.d = self.normal.dot(q)
        self.w = n / n.dot(n)

    def _hit(self, ray, ray_tmin, ray_tmax):
        dn = self.normal.dot(ray.dir)
        if abs(dn) < 1e-8:
            return (False,)
        t = (self.d - self.normal.dot(ray.origin)) / dn
        if t <= ray_tmin or ray_tmax <= t:
            return (False,)

        intersection = ray.at(t)
        hitpt_vector = intersection - self.q
        alpha = self.w.dot(hitpt_vector.cross(self.v))
        beta = self.w.dot(self.u.cross(hitpt_vector))
        if not ((0 < alpha < 1) and (0 < beta < 1)):
            return (False,)
        is_front = ray.dir.dot(self.normal) < 0
        normal = (-1) ** (is_front) * self.normal
        return (True, intersection, normal, t, is_front, self.material, alpha, beta)


class HittableList(Hittable):
    def __init__(self, hittables=[]):
        self.hittables = hittables

    def add(self, hittable):
        self.hittables.append(hittable)

    def remove(self, hittable):
        self.hittables.remove(hittable)

    def clear(self):
        self.hittables = []

    def _hit(self, ray, ray_tmin, ray_tmax):
        hit_anything = False
        closest = ray_tmax
        result = ()
        for hittable in self.hittables:
            did_hit, *tresult = hittable._hit(ray, ray_tmin, closest)
            if did_hit:
                hit_anything = True
                result = tresult
                closest = result[2]

        return hit_anything, *result
