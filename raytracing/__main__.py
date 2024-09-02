from .trace import Camera
from .shapes import *
from .material import *
from .texture import *
from .randfloat import randfloat
from .vec3 import Vec3
import random
import sys


def render_main():
    world = HittableList()
    """
    world.add(Sphere(Vec3(-1, 0, -1), 0.5, Dielectric(1.5)))
    world.add(Sphere(Vec3(-1, 0, -1), 0.4, Dielectric(1 / 1.5)))

    world.add(Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(1, 0, 0), 0.05)))
    world.add(Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))))
    world.add(Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))))
    """
    cam = Camera(
        vfov=20,
        lookfrom=Vec3(13, 2, 3),
        lookat=Vec3(0, 0.2, 0),
        samples_per_pixel=20,
        image_width=800,
        defocus_angle=0,
        focus_dist=10,
    )
    world.add(
        Sphere(
            Vec3(0, -1000, 0),
            1000,
            Lambertian(
                Checkered(
                    0.32,
                    SolidColor(Vec3(0.2, 0.3, 0.1)),
                    SolidColor(Vec3(0.9, 0.9, 0.9)),
                )
            ),
        )
    )
    for a in range(-11, 11):
        for b in range(-11, 11):
            mat = random.random()
            center = Vec3(a + 0.9 * random.random(), 0.2, b + 0.9 * random.random())
            if (center - Vec3(4, 0.2, 0)).length > 0.9:
                if mat < 0.8:
                    albedo = Vec3.random().item_mul(Vec3.random())
                    sphere_material = Lambertian(albedo)
                elif mat < 0.95:
                    albedo = Vec3.random(0.5, 1)
                    fuzz = randfloat(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                else:
                    sphere_material = Dielectric(1.5)
                world.add(Sphere(center, 0.23, sphere_material))
    world.add(Sphere(Vec3(0, 1, 0), 1.0, Dielectric(1.5)))
    world.add(Sphere(Vec3(-4, 1, 0), 1.0, Lambertian(Vec3(0.4, 0.2, 0.1))))
    world.add(Sphere(Vec3(4, 1, 0), 1.0, Metal(Vec3(0.7, 0.6, 0.5), 0.0)))
    cam.render(world)


def render_checkered_balls():
    world = HittableList()
    checker_texture = Checkered(
        0.32, SolidColor(Vec3(0.2, 0.3, 0.1)), SolidColor(Vec3(0.9, 0.9, 0.9))
    )
    world.add(Sphere(Vec3(0, -10, 0), 10, Lambertian(checker_texture)))
    world.add(Sphere(Vec3(0, 10, 0), 10, Lambertian(checker_texture)))
    cam = Camera(
        vfov=20,
        lookfrom=Vec3(13, 2, 3),
        lookat=Vec3(0, 0, 0),
        samples_per_pixel=100,
        image_width=400,
        defocus_angle=0,
    )
    cam.render(world)


def render_globe():
    world_texture = Image("world.png")
    world = Sphere(vec3.Vec3(0, 0, -3), 0.5, Lambertian(world_texture))
    cam = Camera(
        vfov=20,
        samples_per_pixel=1,
        image_width=1024,
        defocus_angle=0,
    )
    cam.render(world)


def render_noise():
    noise_texture = Noise(scale=4, mode="sine", turb_depth=12, albedo=vec3.Vec3(0.5,0.5,0.5))
    world = HittableList()
    world.add(Sphere(Vec3(0, -1000, 0), 1000, Lambertian(noise_texture)))
    world.add(Sphere(Vec3(0, 2, 0), 2, Lambertian(noise_texture)))
    cam = Camera(
        vfov=20,
        lookfrom=Vec3(13, 2, 3),
        lookat=Vec3(0, 0, 0),
        samples_per_pixel=30,
        image_width=400,
        defocus_angle=0,
    )
    cam.render(world)


def render_s():
    world = HittableList()
    world.add(Sphere(Vec3(-1, 0, -1), 0.5, Dielectric(1.5)))
    world.add(Sphere(Vec3(-1, 0, -1), 0.4, Dielectric(1 / 1.5)))

    world.add(Sphere(Vec3(1, 0, -1), 0.5, Metal(Vec3(1, 0, 0), 0.05)))
    world.add(Sphere(Vec3(0, 0, -1), 0.5, Lambertian(Vec3(0.1, 0.2, 0.5))))
    world.add(Sphere(Vec3(0, -100.5, -1), 100, Lambertian(Vec3(0.8, 0.8, 0.0))))
    cam = Camera(
        vfov=20,
        lookfrom=Vec3(-2, 2, 1),
        lookat=Vec3(0, 0, -1),
        image_width=400,
        samples_per_pixel=200,
    )
    cam.render(world)


def main():
    tp = sys.argv[-1]
    if tp not in ["checkered", "main", "globe", "noise", "s"]:
        raise ValueError("unknown:", tp)
    elif tp == "main":
        render_main()
    elif tp == "globe":
        render_globe()
    elif tp == "noise":
        render_noise()
    elif tp == "s":
        render_s()
    else:
        render_checkered_balls()


if __name__ == "__main__":
    main()
