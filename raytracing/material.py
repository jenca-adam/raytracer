from . import ray, randfloat, texture, vec3

BLACK = vec3.Vec3(0,0,0)
WHITE = vec3.Vec3(1,1,1)
class Material:
    def scatter(self, r, hr):
        return False, None, None

    def emit(self, u, v, p):
        return BLACK

class Lambertian(Material):
    def __init__(self, albedo):

        self.albedo = texture.Texture.texturify(albedo)

    def scatter(self, r, hr):
        scatter_dir = hr.normal + vec3.Vec3.random_unit()
        if scatter_dir.near_zero():
            scatter_dir = hr.normal
        scattered_ray = ray.Ray(hr.p, scatter_dir)
        return True, self.albedo.sample(hr.u, hr.v, hr.p), scattered_ray


class Metal(Material):
    def __init__(self, albedo, fuzz):
        self.albedo = texture.Texture.texturify(albedo)
        self.fuzz = min(fuzz, 1)

    def scatter(self, r, hr):
        scatter_dir = vec3.reflect(r.dir, hr.normal)
        scatter_dir = scatter_dir.normalized() + (
            self.fuzz * vec3.Vec3.random_unit()
        )
        scattered_ray = ray.Ray(hr.p, scatter_dir)
        return (
            vec3.dot(scattered_ray.dir, hr.normal) > 0,
            self.albedo.sample(hr.u, hr.v, hr.p),
            scattered_ray,
        )


class Dielectric(Material):
    def __init__(self, refraction_index, albedo=WHITE):
        self.refraction_index = refraction_index
        self.albedo = texture.Texture.texturify(albedo)

    def scatter(self, r, hr):
        ri = 1 / self.refraction_index if hr.front_face else self.refraction_index
        udir = r.dir.normalized()
        cos_theta = min(-vec3.dot(udir, hr.normal), 1)
        sin_theta = (1 - (cos_theta**2)) ** 0.5
        if ri * sin_theta > 1 or reflectance(cos_theta, ri) > randfloat.randfloat():
            scatter_dir = vec3.reflect(udir,hr.normal)
        else:
            scatter_dir = vec3.refract(udir, hr.normal, ri)
        return True, self.albedo.sample(hr.u, hr.v, hr.p), ray.Ray(hr.p, scatter_dir)


class DiffuseLight(Material):
    def __init__(self, e_tex, energy_multiplier=1):
        self.energy_multiplier = energy_multiplier
        self.texture = texture.Texture.texturify(e_tex)

    def emit(self, u, v, p):
        return self.texture.sample(u, v, p) * self.energy_multiplier


def reflectance(cs, ri):
    r0 = ((1 - ri) / (1 + ri)) ** 2
    return r0 + (1 - r0) * (1 - cs) ** 5
