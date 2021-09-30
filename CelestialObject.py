import taichi as ti


@ti.data_oriented
class CelestialObject:
    def __init__(self, dimension=2, N=100, mass=1) -> None:
        # Math contants
        self.PI = ti.atan2(1, 1) * 4
        self.G = ti.field(ti.f32, shape=())
        self.G[None] = 1e-8

        # celestial object related fields
        self.dim = dimension
        self.n = N
        self.m = mass
        self.pos = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.vel = ti.Vector.field(self.dim, ti.f32, shape=self.n)
        self.force = ti.Vector.field(self.dim, ti.f32, shape=self.n)

    def printObj(self):
        str_tmp = "number of bodies: " + str(self.n) + "; mass of bodies: " + str(self.m)
        print(str_tmp)

    def display_2d(self, convas, r=0.005, c=(1, 1, 1)):
        convas.set_background_color((17 / 255, 47 / 255, 65 / 255))
        convas.circles(self.pos, radius=r, color=c)

    @ti.func
    def clearForce(self):
        for i in self.force:
            self.force[i] = ti.Vector([0.0, 0.0])

    @ti.func
    def generateThetaAndR(pi, i, n, min_r):
        assert (min_r < 1) & (min_r > 0)
        theta = 2 * pi * ti.random()  # theta \in (0, 2PI)
        r = (ti.sqrt(ti.random()) * (1 - min_r) + min_r)  # r \in (min_r,1)
        return theta, r

    @ti.kernel
    def initialize_ring(self, c_x: ti.f32, c_y: ti.f32, off_size: ti.f32, init_speed: ti.f32, min_r: float):
        for i in range(self.n):
            if self.n == 1:
                self.pos[i] = ti.Vector([c_x, c_y])
                self.vel[i] = ti.Vector([0.0, 0.0])
            else:
                theta, r = self.generateThetaAndR(self.PI, i, self.n, min_r)
                offset_dir = ti.Vector([ti.cos(theta), ti.sin(theta)])
                center = ti.Vector([c_x, c_y])
                self.pos[i] = center + r * offset_dir * off_size
                self.vel[i] = ti.Vector([-offset_dir[1], offset_dir[0]]) * init_speed

    @ti.kernel
    def initialize_range(self, c_x: ti.f32, c_y: ti.f32, off_size: ti.f32, init_speed: ti.f32):
        for i in range(self.n):
            if self.n == 1:
                self.pos[i] = ti.Vector([c_x, c_y])
                self.vel[i] = ti.Vector([0.0, 0.0])
            else:
                offset = ti.Vector([
                    ti.random() for j in range(self.dim)
                ]) * off_size - ti.Vector([off_size for j in range(self.dim)]) * 0.5
                center = ti.Vector([c_x, c_y])
                self.pos[i] = center + offset
                self.vel[i] = ti.Vector([-offset[1], offset[0]]) * init_speed

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
