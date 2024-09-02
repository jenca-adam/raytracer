from . import aabb, shapes, randfloat
import sys

class BVH(shapes.Hittable):
    def __init__(self, objects, start, end):
        self.obj=objects
        self.start=start
        self.end=end
        self.bbox = aabb.AABB.empty()
        for i in objects[start:end]:
            self.bbox=aabb.AABB.merge(self.bbox,i.bounding_box())

        axis = self.bbox.longest_axis()
        comparator = self.box_compare(axis)
        length = end - start
        if length == 1:
            self.left = self.right = self.obj[start]
        elif length == 2:
            self.left = self.obj[start]
            self.right = self.obj[start + 1]
        else:
            self.obj.sort(key=comparator)
            mid = start + length // 2
            self.left = BVH(self.obj, start, mid)
            self.right = BVH(self.obj, mid, end)
        #self.bbox = aabb.AABB.merge(self.left.bounding_box(), self.right.bounding_box())
    @classmethod
    def from_hittable_list(cls, hl):
        return cls(hl.hittables, 0, len(hl))

    def _hit(self, ray, ray_tmin, ray_tmax):
        if not self.bbox.hit(ray, ray_tmin, ray_tmax):
            return (False,)
        hit_left, *hr = self.left._hit(ray, ray_tmin, ray_tmax)
        hit_right, *hr2 = self.right._hit(
            ray, ray_tmin, hr[2] if hit_left else ray_tmax
        )
        if hit_right:
            return True, *hr2
        return (hit_left or hit_right), *hr

    def bounding_box(self):
        return self.bbox

    def box_compare(self, axis):
        return lambda a: a.bounding_box()[axis].start
