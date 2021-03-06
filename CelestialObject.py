import taichi as ti

@ti.data_oriented
class CelestialObject:
    def __init__(self, dimension=2, N=100, mass=1) -> None:
        # Math contants
        self.PI = ti.atan2(1, 1) * 4
        self.G = ti.field(ti.f32, shape=())

        # celestial object related fields
        self.dim = dimension
        self.n = N
        self.m = mass
        self.pos = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.vel = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.force = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.color = ti.Vector.field(3, ti.f32, shape=self.n)

    def display(self, canvas, scene, camera, r=0.005, c=(1, 1, 1)):
        canvas.set_background_color((17 / 255, 47 / 255, 65 / 255))
        if self.dim == 2:
            canvas.circles(self.pos, radius=r, color=c)
        elif self.dim == 3:
            scene.set_camera(camera)
            scene.ambient_light((0, 0, 0))
            scene.particles(self.pos, radius=r, color=c)
            scene.point_light(pos=(0.5, 1.5, 0.5), color=(0.5, 0.5, 0.5))
            scene.point_light(pos=(0.5, 1.5, 1.5), color=(0.5, 0.5, 0.5))
            canvas.scene(scene)

    @ti.func
    def clearForce(self):
        for i in self.force:
            self.force[i] = ti.Vector([0.0 for j in range(self.dim)])

    @ti.kernel
    def initialize_range(self, pos_center: ti.template(), off_size: ti.f32, init_speed: ti.f32):
        for i in range(self.n):
            if self.n == 1:
                self.pos[i] = pos_center
                self.vel[i] = ti.Vector([0.0 for j in range(self.dim)])
            else:
                offset = ti.Vector([ti.random() for j in range(self.dim)]) * off_size - ti.Vector([off_size for j in range(self.dim)]) * 0.5
                self.pos[i] = pos_center + offset
                # self.vel[i] = ti.Vector([ti.random() for j in range(self.dim)]) * init_speed # 如何统一2/3d初速度方向？
                self.vel[i] = ti.Vector([-offset[1], offset[0], 0.0] if self.dim == 3 else [-offset[1], offset[0]] if self.dim == 2 else [0.0 for j in range(self.dim)]) * init_speed # 2d初速度严格，3d初速度选在xoy平面上

    @ti.kernel
    def computeForce(self):
        self.clearForce()
        for i in range(self.n):
            p = self.pos[i]
            for j in range(self.n):
                if j != i:
                    diff = self.pos[j] - p
                    r = diff.norm(1e-2)
                    self.force[i] += self.G[None] * self.m * self.m * diff / r**3

    @ti.kernel
    def update(self, h: ti.f32):
        for i in self.vel:
            self.vel[i] += h * self.force[i] / self.m
            self.pos[i] += h * self.vel[i]
