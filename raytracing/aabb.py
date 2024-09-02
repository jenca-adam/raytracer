from . import interval
import sys


class AABB:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.axes = [x, y, z]

    def __getitem__(self, i):
        return self.axes[i]

    @classmethod
    def from_points(cls, a, b):
        x = (
            interval.Interval(a[0], b[0])
            if a[0] <= b[0]
            else interval.Interval(b[0], a[0])
        )
        y = (
            interval.Interval(a[1], b[1])
            if a[1] <= b[1]
            else interval.Interval(b[1], a[1])
        )
        z = (
            interval.Interval(a[2], b[2])
            if a[2] <= b[2]
            else interval.Interval(b[2], a[2])
        )
        return cls(x, y, z)

    @classmethod
    def merge(cls, a, b):
        return cls(
            interval.Interval.merge(a.x, b.x),
            interval.Interval.merge(a.y, b.y),
            interval.Interval.merge(a.z, b.z),
        )

    @classmethod
    def empty(cls):
        return cls(
            interval.Interval.empty, interval.Interval.empty, interval.Interval.empty
        )

    def hit(self, ray, ray_tmin, ray_tmax):
        ray_orig, ray_dir = ray.origin, ray.dir
        intervals = (self.x, self.y, self.z)
        for axis in range(3):
            ax = intervals[axis]
            adi = 1 / ray_dir[axis]
            t0 = (ax.start - ray_orig[axis]) * adi
            t1 = (ax.end - ray_orig[axis]) * adi
            if t0 < t1:
                if t0 > ray_tmin:
                    ray_tmin = t0
                if t1 < ray_tmax:
                    ray_tmax = t1
            else:
                if t1 > ray_tmin:
                    ray_tmin = t1
                if t0 < ray_tmax:
                    ray_tmax = t0
            if ray_tmax <= ray_tmin:
                return False
        return True
    def longest_axis(self):
        return max(range(3), key=self.axes.__getitem__)
       
