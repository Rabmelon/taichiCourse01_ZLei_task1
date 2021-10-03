import taichi as ti


@ti.data_oriented
class CelestialObject:
    def __init__(self, dimension=2, N=100, mass=1) -> None:
        # Math contants
        self.PI = ti.atan2(1, 1) * 4
        self.G = ti.field(ti.f32, shape=())
        self.G[None] = 1e-3

        # celestial object related fields
        self.dim = dimension
        self.n = N
        self.m = mass
        self.pos = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.vel = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.force = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.color = ti.Vector.field(3, ti.f32, shape=self.n)

        # assist

    def printObj(self):
        str_tmp = "number of bodies: " + str(self.n) + "; mass of bodies: " + str(self.m)
        print(str_tmp)

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

    @ti.func
    def generateThetaAndR(pi, i, n, min_r):
        assert (min_r < 1) & (min_r > 0)
        theta = 2 * pi * ti.random()  # theta \in (0, 2PI)
        r = (ti.sqrt(ti.random()) * (1 - min_r) + min_r)  # r \in (min_r,1)
        return theta, r

    @ti.kernel # 生成环/球壳形状的初始分布
    def initialize_ring(self, c_x: ti.f32, c_y: ti.f32, off_size: ti.f32, init_speed: ti.f32, min_r: ti.f32):
        for i in range(self.n):
            if self.n == 1:
                self.pos[i] = ti.Vector([c_x, c_y])
                self.vel[i] = ti.Vector([0.0, 0.0])
            else:
                theta, r = self.generateThetaAndR(self.PI, i, self.n, min_r)
                offset_dir = ti.Vector([ti.cos(theta), ti.sin(theta)])
                center = ti.Vector([c_x, c_y])
                self.pos[i] = center + r * offset_dir * off_size
                self.pos[i] = ti.Vector([ti.random() for j in range(self.dim)]) * init_speed # 如何统一2/3d初速度方向？
                # self.vel[i] = ti.Vector([-offset[1], offset[0]]) * init_speed

    @ti.kernel # 生成正方形/立方体形状的初始分布
    def initialize_range(self, pos_center: ti.template(), off_size: ti.f32, init_speed: ti.f32):
        for i in range(self.n):
            if self.n == 1:
                self.pos[i] = pos_center
                self.vel[i] = ti.Vector([0.0 for j in range(self.dim)])
            else:
                offset = ti.Vector([ti.random() for j in range(self.dim)]) * off_size - ti.Vector([off_size for j in range(self.dim)]) * 0.5
                self.pos[i] = pos_center + offset
                self.pos[i] = ti.Vector([ti.random() for j in range(self.dim)]) * init_speed # 如何统一2/3d初速度方向？
                # self.vel[i] = ti.Vector([-offset[1], offset[0]]) * init_speed

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
