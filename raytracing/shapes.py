from collections import namedtuple
import math,sys
from . import aabb,vec3

"""HitResult = namedtuple(
    "HitResult",
    ("p", "normal", "t", "front_face", "material", "u", "v"),
    defaults=(None, None, None, None, None, None, None),
)"""
log=open("hcc_normal.log",'w')
class HitResult:
    def __init__(self, p=None, normal=None, t=None, front_face=None, material=None, u=None, v=None):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.material = material
        self.u = u
        self.v = v
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
        rvec = vec3.array([radius, radius, radius])
        self.bbox = aabb.AABB.from_points(center - rvec, center + rvec)

    def _hit(self, ray, ray_tmin, ray_tmax, *args):
        oc = self.center - ray.origin
        a = ray.dir.length_squared 
        h = vec3.dot(ray.dir, oc)
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
        is_front = vec3.dot(ray.dir, outward_normal) < 0
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
        theta, phi = math.acos(-p[1]), math.atan2(-p[2], p[0]) + math.pi
        u = phi / (2 * math.pi)
        v = theta / math.pi
        return u, v

    def bounding_box(self):
        return self.bbox


class Quad(Hittable):
    def __init__(self, q, u, v, material):
        n = vec3.cross(u, v)
        self.q = q
        self.u = u
        self.v = v
        self.material = material
        self.normal = n / vec3.linalg.norm(n)
        self.d = vec3.dot(self.normal, q)
        self.w = n / vec3.dot(n, n)

    def _hit(self, ray, ray_tmin, ray_tmax):
        dn = vec3.dot(self.normal, ray.dir)
        if abs(dn) < 1e-8:
            return (False,)
        t = (self.d - vec3.dot(self.normal, ray.origin)) / dn
        if t <= ray_tmin or ray_tmax <= t:
            return (False,)

        intersection = ray.at(t)
        hitpt_vector = intersection - self.q
        alpha = vec3.dot(self.w, vec3.cross(hitpt_vector, self.v))
        beta = vec3.dot(self.w, vec3.cross(self.u, hitpt_vector))
        if not ((0 < alpha < 1) and (0 < beta < 1)):
            return (False,)
        is_front = vec3.dot(ray.dir, self.normal) < 0
        normal = (-1) ** (is_front) * self.normal
        return (True, intersection, normal, t, is_front, self.material, alpha, beta)


class HittableList(Hittable):
    def __init__(self, hittables=[]):
        self.hittables = hittables
        self.hcc = 0
        self.bbox = aabb.AABB.empty()

    def add(self, hittable):
        self.hittables.append(hittable)
        self.bbox = aabb.AABB.merge(self.bbox, hittable.bounding_box())

    def clear(self):
        self.hittables = []
        self.bbox = aabb.AABB.empty

    def _hit(self, ray, ray_tmin, ray_tmax):
        self.hcc+=1
        print("HC Calls(no BVH)", self.hcc, file=log)
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

    def bounding_box(self):
        return self.bbox

    def __len__(self):
        return len(self.hittables)
