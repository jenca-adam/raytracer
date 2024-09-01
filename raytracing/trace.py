from . import ray, vec3, ppm, shapes, interval, material
import tqdm
import random
import math
from functools import lru_cache


class Camera:
    def __init__(
        self,
        aspect_ratio=16 / 9,
        samples_per_pixel=15,
        vfov=45,
        lookfrom=vec3.Vec3(0, 0, 0),
        lookat=vec3.Vec3(0, 0, -1),
        vup=vec3.Vec3(0, 1, 0),
        max_bounces=20,
        image_width=400,
        defocus_angle=0,
        focus_dist=10,
    ):  #
        self.aspect_ratio = aspect_ratio
        self.samples_per_pixel = samples_per_pixel

        self.vfov = vfov
        self.lookfrom = lookfrom
        self.lookat = lookat
        self.vup = vup
        self.theta = math.radians(self.vfov)
        self.h = math.tan(self.theta / 2)
        self.iw = image_width
        self.ih = int(max(self.iw // self.aspect_ratio, 1))
        self.focal_length = (lookfrom - lookat).length
        self.w = (lookfrom - lookat).normalized()
        self.u = self.vup.cross(self.w).normalized()
        self.v = self.w.cross(self.u)
        self.focus_dist = focus_dist
        self.defocus_angle = defocus_angle

        self.viewport_height = 2 * self.h * self.focus_dist
        self.viewport_width = self.viewport_height * (self.iw / self.ih)
        self.camera_center = self.lookfrom
        self.viewport_u = self.viewport_width * (self.u)
        self.viewport_v = self.viewport_height * (-self.v)
        self.pixel_delta_u = self.viewport_u / self.iw
        self.pixel_delta_v = self.viewport_v / self.ih
        self.viewport_upper_left = (
            self.camera_center
            - self.focus_dist * self.w
            - self.viewport_u / 2
            - self.viewport_v / 2
        )
        self.pixel_start = (
            self.viewport_upper_left + (self.pixel_delta_u + self.pixel_delta_v) * 0.5
        )
        self.defocus_radius = focus_dist * math.tan(
            math.radians(self.defocus_angle / 2)
        )
        self.defocus_disk_u = self.u * self.defocus_radius
        self.defocus_disk_v = self.v * self.defocus_radius

        self.max_bounces = max_bounces

    def ray_color(self, r, world, bounces):
        if bounces == 0:
            return vec3.Vec3(0, 0, 0)
        did_hit, res = world.hit(r, 0.001, float("inf"))

        if did_hit:
            did_reflect, attenuation, scattered = res.material.scatter(r, res)
            if did_reflect:
                # print(attenuation,scattered, file=__import__("sys").stderr)
                return attenuation.item_mul(
                    self.ray_color(scattered, world, bounces - 1)
                )
            else:
                return vec3.Vec3(0, 0, 0)
            # direction = res.normal + vec3.Vec3.random_unit()
            # return 0.5 * self.ray_color(ray.Ray(res.p, direction), world, bounces - 1)
            # return 0.5 * (res.normal + vec3.Vec3(1, 1, 1))
        udir = r.dir.normalized()
        a = 0.5 * (udir.y + 1.0)
        return (1.0 - a) * vec3.Vec3(1.0, 1.0, 1.0) + a * vec3.Vec3(0.5, 0.7, 1.0)

    def render(self, world):
        self.pixel_samples_scale = 1 / self.samples_per_pixel
        ppm.write_header(self.iw, self.ih)
        for j in tqdm.tqdm(range(self.ih)):
            for i in range(self.iw):
                pixel_pos = (
                    self.pixel_start
                    + (i * self.pixel_delta_u)
                    + (j * self.pixel_delta_v)
                )
                pixel_color = (
                    sum(
                        (
                            self.ray_color(
                                self.get_ray(i, j), world, self.max_bounces
                            ).clamp_all(interval.Interval(0, 0.999))
                            for sample in range(self.samples_per_pixel)
                        ),
                        vec3.Vec3(0, 0, 0),
                    )
                    * self.pixel_samples_scale
                )
                ppm.write_color(*pixel_color.gamma_corrected().asrgb())

    def get_ray(self, i, j):
        offset = vec3.Vec3(random.random() - 0.5, random.random() - 0.5, 0)
        pixel_pos = (
            self.pixel_start
            + ((i + offset.x) * self.pixel_delta_u)
            + ((j + offset.y) * self.pixel_delta_v)
        )
        ray_origin = (
            self.camera_center if self.defocus_angle <= 0 else self.sample_defocus()
        )
        return ray.Ray(ray_origin, pixel_pos - self.camera_center)

    def sample_defocus(self):
        p = vec3.Vec3.random_in_unit_disk()
        return (
            self.camera_center
            + (p.x * self.defocus_disk_u)
            + (p.y * self.defocus_disk_v)
        )
